
package main

import (
	"fmt"
	"github.com/stianeikeland/go-rpio"
	"math/rand"
	"strconv"
	"time"
	"encoding/json"
	"os"
	"os/exec"
	"io/ioutil"
	// sudo apt-get install libasound2-dev
	// go get github.com/faiface/beep
	// go get ./...
	"github.com/faiface/beep"
	"github.com/faiface/beep/speaker"
	"github.com/faiface/beep/vorbis"
	"github.com/faiface/beep/wav"
	"github.com/faiface/beep/mp3"
)

type Config struct {
	Serial int
	DialerType string
	DialerYellowGpio int
	DialerRedGpio int
	DialerLogic bool
	HookGpio   int
	HookPower  string
	HookLogic bool

	PadRowGpios   []int
	PadColGpios   []int
}

var Playing = false
var Random1 *rand.Rand

func init() {
	err := rpio.Open()
	if err != nil {
		panic(err)
	}

	s1 := rand.NewSource(time.Now().UnixNano())
	Random1 = rand.New(s1)

}


func main() {


	// static config
	bts, err := ioutil.ReadFile("config.json")
	if err != nil {
		panic(err)
	}
	var config Config

	json.Unmarshal(bts, &config)

	if config.HookGpio == 0 {
		panic("Bad config.json")
	}

	// music files
	mts, err := ioutil.ReadFile("music.json")
	if err != nil {
		panic(err)
	}
	var music []string

	json.Unmarshal(mts, &music)
	if len(music) < 10 {
		panic("Bad music.json")

	}

	// action type
	ats, err := ioutil.ReadFile("action.json")
	if err != nil {
		panic(err)
	}
	type Action struct { Action string }
	var action Action

	json.Unmarshal(ats, &action)
	if len(action.Action) == 0 {
		panic("Bad action.json")
	}


	// volume
	vts, err := ioutil.ReadFile("volume.json")
	if err != nil {
		panic(err)
	}
	type Volume struct { Volume string }
	var volume Volume

	json.Unmarshal(vts, &volume)
	if volume.Volume == "" {
		panic("Bad volume.json")
	}
	setvolume(volume.Volume)

	//go PhoneHome(config, action, music)
	
	// set up the hook
	isOnHook := true
	hkc := make(chan bool)
	go onhook(hkc, config.HookGpio, config.HookPower, config.HookLogic)

	// set up the dialertype
	dgc := make(chan int)
	switch config.DialerType {
	 case "rotator2":
		go rotator2(dgc, config.DialerYellowGpio, config.DialerRedGpio)
	 case "keypad1":
		go keypad1(dgc, config.PadRowGpios, config.PadColGpios)
	 case "keypad2":
		go keypad2(dgc, config.PadRowGpios, config.PadColGpios)
	 default: panic("Bad DialerType in config.json")
	}



	// mainloop
	for {
		select {
		case isOnHook = <-hkc:
			fmt.Println("mainloop onhook, playing: ", isOnHook, Playing)
			if isOnHook && Playing {
				Playing = false
				continue
			}
			if !isOnHook &&  !Playing {
				go play("kiestoon.ogg")
				continue
			}
			
		case d := <-dgc:
			fmt.Println("dialed: ", d, Playing)
			if Playing {
				done <- true
				time.Sleep(500 * time.Millisecond)
			}
			if isOnHook == false {
				go play (SelectMusic(d, action.Action, music))
			}
		}
	}
}

var PreviousMusic = -1

func SelectMusic(d int, action string, music []string) string {
	switch action {
	 case "loop":
		PreviousMusic++
		if PreviousMusic == len(music) {
			PreviousMusic = 0
		}
		return music[PreviousMusic]
	 case "standaard":		// backward compat.
		fallthrough
	 case "bynumber":
		fmt.Println("SelectMusic ", d-1)
		return music[d-1]
	 case "random":
		for {
			i := Random1.Intn(len(music))
			if i == PreviousMusic {
				continue
			}
			fmt.Println("random: ", i)
			PreviousMusic = i
			return music[i]
		}
	 default:
		panic("Bad Action in config.json")
	}
	return ""
}


func rotator2(digitchan chan int, fison, fstep int) {
	step := rpio.Pin(fstep) // 19
	ison := rpio.Pin(fison) //26

	step.Output()
        step.High()
	ison.Output()
        ison.High()

	for {
		io := ison.Read()
		if io == 1 {
			time.Sleep(0* time.Millisecond) // calls Gosched, must do
			continue		
		}

		fmt.Println("starting")
		time.Sleep(100* time.Millisecond)   // prevent 0 pulses
		pulse := 0
		swap := 0

		for {
			v := step.Read()
			if swap == 0 && v == 1 {
				swap = 1
				continue
			}

			if swap == 1 && v == 0 {
				swap = 0
				pulse = pulse + 1
				fmt.Println("add pulto to ", pulse)
				continue
			}

			
			io := ison.Read()
			if io == 1 {				// did the dailing stop?
				fmt.Println("got ", pulse)
				if pulse < 1 {
					fmt.Println("pulse forced to 1")
					pulse = 1
				}
				if pulse > 10 {
					fmt.Println("pulse forced to 10")
					pulse = 10
				}
				digitchan <- pulse
				//time.Sleep(1000 * time.Millisecond)
				break
			}

			time.Sleep(1* time.Millisecond)		// somewhat rest, to be decided.....


		}
	}
}

func rotator1(digitchan chan int, pin, speed int) {
	step := rpio.Pin(pin)

	step.Output()
        step.High()

	fmt.Println(speed)
	if speed == 0 {
	
		speed=2000
	}
	fmt.Println(speed)

	for {
		v := step.Read()
		if v == 1 {
			time.Sleep(300 * time.Millisecond)
			continue
		}

		fmt.Println("starting")
		t0 := time.Now()
		pulse := 0
		swap := 0

		for {
			v := step.Read()
			if swap == 0 && v == 1 {
				swap = 1
				continue
			}

			if swap == 1 && v == 0 {
				swap = 0
				pulse = pulse + 1
				fmt.Println("add pulto to ", pulse)
				continue
			}

			t := time.Now().Sub(t0)
			//if t > 2000000000 {
			if int(t) > speed * 1000000 {
				switch {
				case pulse < 1:
					pulse = 1
				case pulse > 10:
					pulse = 10
				}
				fmt.Println("sending ", pulse)
				digitchan <- pulse
				time.Sleep(1000 * time.Millisecond)
				break
			}
			time.Sleep(10 * time.Millisecond)

		}
	}
}

var isOnHook bool

func onhook(hookchan chan bool, pin int, power string, hooklogic bool) {
	fmt.Println(pin)
	hook := rpio.Pin(pin)

	testHighLow := rpio.Low
	

	switch power {
	 case "3.3V":
		testHighLow = rpio.High
		hook.Input()
		rpio.PullMode(hook, rpio.PullDown)
	 case "Ground":
		testHighLow = rpio.Low
		hook.Output()
		hook.High()
         default:
		panic("HoogLogic: bad value in config.json [3.3V or Ground]")
	}

	if hooklogic {
		testHighLow = rpio.Low
	} else {
		testHighLow = rpio.High
	}

	ov := hook.Read()
	isOnHook = ov == testHighLow
	hookchan <- isOnHook

	for {
		v := hook.Read()
		if ov != v {
			ov = v
			isOnHook = ov == testHighLow
			fmt.Println("sending from onhook ", isOnHook)
			hookchan <- isOnHook
		}
		time.Sleep(time.Millisecond * 100)
	}
}

func readkey1(row, col []int) string {
	var keypad = [][]string{{"1", "2", "3"},{"4", "5", "6"},{"7","8","9"},{"", "0", ""}}

	colpin := make([]rpio.Pin, 0)
	rowpin := make([]rpio.Pin, 0)

	// Set all columns as output low
	for _, j := range col {
		p := rpio.Pin(j)
		p.Output()
		p.Low()
		colpin = append(colpin, p)
	}
	// Set all rows as input
	for _, j := range row {
		p := rpio.Pin(j)
		p.Input()
		rpio.PullMode(p, rpio.PullUp)
		rowpin = append(rowpin, p)
	}

	// Scan rows for pushed key/button
	// A valid key press should set "rowVal"  between 0 and 3.
	rowVal := -1
	for i, p := range rowpin {
		if p.Read() == 0 {
			rowVal = i
		}
	}

	// if rowVal is not 0 thru 3 then no button was pressed and we can exit
	if rowVal < 0 || rowVal > 3 {
		return ""
	}

	// Convert columns to input
	colpin = make([]rpio.Pin, 0) // reset
	for _, j := range col {
		p := rpio.Pin(j)
		p.Input()
		rpio.PullMode(p, rpio.PullDown)
		colpin = append(colpin, p)
	}

	// Switch the i-th row found from scan to output
	p1 := rpio.Pin(row[rowVal])
	p1.Output()
	p1.High()

	colVal := -1
	for i, p := range colpin {
		t := p.Read()
		if t == 1 {
			colVal = i
		}
	}

	// if colVal is not 0 thru 2 then no button was pressed and we can exit
	if colVal < 0 || colVal > 2 {
		return ""
	}

	return keypad[rowVal][colVal]

}

func readkey2(row, col []int) string {
	var keypad = [][]string{{"1", "2", "3"},{"4", "5", "6"},{"7","8","9"},{"", "0", ""}}

	rowpin := make([]rpio.Pin, 0)
	colpin := make([]rpio.Pin, 0)

	for _, j := range col {
		p := rpio.Pin(j)
		p.Output()
		p.High()
		colpin = append(colpin, p)
	}
	for _, j := range row {
		p := rpio.Pin(j)
		p.Output()
		p.High()
		rowpin = append(rowpin, p)
	}

	xx := -1
	for i, p := range rowpin {
		if p.Read() == 0 {
			xx = i
		}
	}
	yy := -1
	for i, p := range colpin {
		if p.Read() == 0 {
			yy = i
		}
	}
	if xx != -1 &&  yy != -1 {
		return keypad[xx][yy]
	}

	return ""
		

}

// 3 x 4 pad no earth, 3 x 4 wires
func keypad1(digitchan chan int, row, col []int) {
	for {
		n := readkey1(row, col)
		if n != "" {
			digit, _ := strconv.Atoi(n)
			digit++
			switch {
			case digit < 1:
				digit = 1
			case digit > 10:
				digit = 10
			}
			digitchan <- digit
		}
		time.Sleep(time.Millisecond * 300)
	}
}

// 3 x 4 pad earth,   4 switches around, 1 earth (white)
func keypad2(digitchan chan int, row, col []int) {
	for {
		n := readkey2(row, col)
		if n != "" {
			digit, _ := strconv.Atoi(n)
			digit++
			switch {
			case digit < 1:
				digit = 1
			case digit > 10:
				digit = 10
			}
			digitchan <- digit
		}
		time.Sleep(time.Millisecond * 300)
	}
}

var done = make(chan bool)

func play(mf string) {
	f, err := os.Open("music/" + mf)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	Playing = true

	var s beep.StreamSeekCloser
	var format beep.Format

	switch mf[len(mf)-4:] {
	 case ".wav":
		s, format, _ = wav.Decode(f)
	 case ".ogg":
		s, format, _ = vorbis.Decode(f)
	 case ".mp3":
		s, format, _ = mp3.Decode(f)
	}
	
	speaker.Init(format.SampleRate, format.SampleRate.N(time.Second/2))

	speaker.Play(beep.Seq(s, beep.Callback(func() {
		Playing = false // normal end
	})))
	fmt.Println("waiting ", mf)

	for {
		select {
		case <-done:
			fmt.Println("got done")
			goto einde
		default:
			if Playing == false {
				fmt.Println("play default Playing == false")
				goto einde
			}
			if isOnHook {
				fmt.Println("play default onhook == true")
				goto einde
			}
		}
	}
einde:

	Playing = false
	fmt.Println("closing ", mf)
	s.Close()
}

func setvolume(v string) {
	vcmd := exec.Command("./vol.py", v)
        vcmd.Start()
        vcmd.Wait()
	
}
