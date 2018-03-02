extern crate bluetooth_serial_port;
extern crate sysfs_gpio;

use std::{thread};
use std::time::Duration;
use std::thread::sleep;
use std::io;
use std::io::{Read, Write};
use std::str;

use sysfs_gpio::{Direction, Pin};

use bluetooth_serial_port::{BtProtocol, BtSocket, BtDevice};

fn main() {
    thread::spawn(|| check_bluetooth());
    
    loop {
        let mut input = String::new();

        io::stdin().read_line(&mut input)
         .expect("Failed to read line");

         if input.trim().to_uppercase() == "B" {
            match blink_led(21) {
                Ok(()) => println!("Success!"),
                Err(err) => println!("We have a blinking problem: {}", err),
            }
         }

         if input.trim().to_uppercase() == "C" {
            match blink_led(16) {
                Ok(()) => println!("Success!"),
                Err(err) => println!("We have a buzzing problem: {}", err),
            }
         }

        if input.trim().to_uppercase() == "Q" {
            break;
        }
    }
}

fn blink_led(pin: u64) -> sysfs_gpio::Result<()> {
	let my_led = Pin::new(pin);

    my_led.with_exported(|| {
        sleep(Duration::from_millis(500));
		
        my_led.set_direction(Direction::Low)?;
        for _ in 0..5 {
            my_led.set_value(0)?;
            sleep(Duration::from_millis(100));
            my_led.set_value(1)?;
            sleep(Duration::from_millis(100));
        }
        my_led.set_value(0)?;
		Ok(())
    })
}

fn check_bluetooth() {
    
    loop {
		let mut socket= BtSocket::new(BtProtocol::RFCOMM).unwrap();
		let mut buffer = [0; 30];
		let num_bytes_read = socket.read(&mut buffer[..]).unwrap();
		//let num_bytes_written = socket.write(&buffer[0..num_bytes_read]).unwrap();
		println!("Read `{}` bytes buffer {:?}", num_bytes_read, buffer);
		
		 let s = match str::from_utf8(&buffer) {
			Ok(v) => v,
			Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
		};

		println!("result: {}", s)
	}
}
