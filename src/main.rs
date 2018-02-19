use std::{thread};
use std::time::Duration;
use std::io;
use std::io::{Read, Write};
use std::str;

extern crate bluetooth_serial_port;

use bluetooth_serial_port::{BtProtocol, BtSocket, BtDevice};

fn main() {
    thread::spawn(|| check_bluetooth());

    loop {
        let mut input = String::new();

        io::stdin().read_line(&mut input)
         .expect("Failed to read line");

        if input.trim().to_uppercase() == "Q" {
            break;
        }
    }
}

fn check_bluetooth() {
	let mut devices: Vec<BtDevice>;
	
	loop {
		devices = bluetooth_serial_port::scan_devices().unwrap();
		println!("Devices {}",devices.len());
	 
		if devices.len() > 0 {
			break;
		}
		
		thread::sleep(Duration::from_millis(4000));
	}
    let device = &devices[0];
   
	let mut socket = BtSocket::new(BtProtocol::RFCOMM).unwrap();
    socket.connect(device.addr).unwrap();

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
