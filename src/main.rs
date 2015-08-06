extern crate clap;

use clap::{App, SubCommand};

fn main() {
    let m = App::new("ctx")
        .about("A CLI utility to manage context")
        .author("Kevin Qiu <kevin@idempotent.ca>")
        .subcommand_required(true)
        .subcommand(SubCommand::with_name("switch"))
            .about("Switch context")
        .get_matches();

    match m.subcommand() {
    }
}
