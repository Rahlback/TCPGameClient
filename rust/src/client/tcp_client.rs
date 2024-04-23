
use std::io::prelude::*;
use std::net::TcpStream;

pub struct TCPClient {
    stream: TcpStream,
    name: String,
    user_id: u32
}


impl TCPClient {
    pub fn get_message(&mut self) -> Vec<u8>{
        let mut buffer_l: [u8; 4] = [0; 4];

        let res  = self.stream.read_exact(&mut buffer_l); //  Result<usize, std::io::Error>
        
        let mut message_length: u32 = 0; // buffer_l[3] << 24 + buffer_l[2] << 16 + buffer_l[1] << 8 + buffer_l[0];
        let mut offset = 24;
        for x in buffer_l {
            message_length += u32::from(x) << offset;
            offset -= 8;
        }

        let mut buffer_t: [u8; 10000] = [0; 10000];
        let range = usize::try_from(message_length).unwrap();
        let full_read_res = self.stream.read(&mut buffer_t[0..range]);

        // let s = from_utf8(&buffer_t[0..range]).unwrap();

        // println!("Received: {:?} = {}", buffer_l, message_length);
        // println!("  Message: {:?}", s);

        // self.stream.read_to_string(buf)
        if res.is_err() {
            println!("TCPClient: Something went wrong! {}", res.err().unwrap().to_string());
        }

        if full_read_res.is_err() {
            println!("Failed to read TCPStream");
        }
        return buffer_t[0..range].to_vec();
    }

    pub fn register(&mut self, name: &str, user_id: u32, big_endian : u32) -> () {
        self.name = name.to_string();
        self.user_id = user_id;
        let register_message = format!("REGISTER:user_id={user_id},name={name},big_endian={big_endian}");
        
        println!("Sending message: {}", register_message);
        let _ = self.stream.write_all(register_message.as_bytes());

        let response = self.get_message();

        if response.is_ascii() {
            println!("{}", String::from_utf8(response).expect("Error"));
        }
    }

    pub fn send_message(&mut self, message: String) -> Result<(), std::io::Error> {
        println!("Sending: {}", &message);
        return self.stream.write_all(message.as_bytes());      
    }

}

pub fn connect_to_server(server_ip: &str, server_port: &str) -> Result<TCPClient, String> {
    let client = TcpStream::connect(format!("{server_ip}:{server_port}"));
    
    match &client {
        Ok(_) => Ok(TCPClient {stream: client.unwrap(), name: "RustDefault".to_string(), user_id: 0}),
        Err(eh) => Err(format!("Failure to connect: {}", eh.to_string()))
    }
}
