package main

import (
	"fmt"
	"time"
)

func exampleGoroutine() {
	go func() {
		fmt.Println("hi")
	}()
	time.Sleep(100 * time.Millisecond)
}

func exampleChannels() {
	ch := make(chan int)

	go func() {
		fmt.Println("[Sender] Sending 42...")
		ch <- 42
		fmt.Println("[Sender] 42 sent!")
	}()

	go func() {
		fmt.Println("[Receiver] Wating for data")
		value := <-ch
		fmt.Println("[Receiver] Got Value: ", value)
	}()

	time.Sleep(1 * time.Millisecond)
}

func exampleSelect() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(1 * time.Millisecond)
		ch1 <- "[ch1] Hello from channel 1!"
	}()

	go func() {
		time.Sleep(2 * time.Millisecond)
		ch2 <- "[ch2] Hello from channel 1!"
	}()

	// Use select to wait for whichever channel is ready first
	select {
	case msg1 := <-ch1:
		fmt.Println("Received from ch1:", msg1)
	case msg2 := <-ch2:
		fmt.Println("Received from ch2:", msg2)
	default:
		fmt.Println("No channel was ready immediately.")
	}

	// If you want to receive from both channels eventually, you can do a loop:
	fmt.Println("Now let's receive from both channels (not just first):")
	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-ch1:
			fmt.Println("Received from ch1:", msg1)
		case msg2 := <-ch2:
			fmt.Println("Received from ch2:", msg2)
		}
	}
}

func main() {
	exampleGoroutine()
	exampleChannels()
	exampleSelect()
}
