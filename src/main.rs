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

	match blink_led() {
                Ok(()) => println!("Success!"),
                Err(err) => println!("We have a blinking problem: {}", err),
    }

    loop {
        let mut input = String::new();

        io::stdin().read_line(&mut input)
         .expect("Failed to read line");

        if input.trim().to_uppercase() == "Q" {
            break;
        }
    }
}

fn blink_led() -> sysfs_gpio::Result<()> {
	let my_led = Pin::new(21);

    my_led.with_exported(|| {
        sleep(Duration::from_millis(500));
		
        my_led.set_direction(Direction::Low)?;
        for _ in 0..200 {
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
	let mut devices: Vec<BtDevice>;
    let device: &BtDevice;
    let mut socket: BtSocket;
	
	loop {
		devices = bluetooth_serial_port::scan_devices().unwrap();
		println!("Devices {}",devices.len());
	 
		if devices.len() > 0 {
			device = &devices[0];
   
	        socket = BtSocket::new(BtProtocol::RFCOMM).unwrap();
            socket.connect(device.addr).unwrap();

            break;
		}		
		thread::sleep(Duration::from_millis(4000));
	}
    
    loop {
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
