#!/usr/bin/expect

# see in: http://stackoverflow.com/a/36296872

set auth_code "[lindex $argv 0]"
set email_add "[lindex $argv 1]"
set address "[lindex $argv 2]"
set subject "[lindex $argv 3]"
set ts_date "[lindex $argv 4]"
set ts_time "[lindex $argv 5]"

set timeout 10
spawn openssl s_client -connect smtp.gmail.com:465 -crlf -ign_eof 

expect "220" {
  send "EHLO localhost\n"

  expect "250" {
    send "AUTH PLAIN $auth_code\n"

    expect "235" {
      send "MAIL FROM: <$email_add>\n"

      expect "250" {
        send "RCPT TO: <$address>\n"

        expect "250" {
          send "DATA\n"

          expect "354" {
            send "Subject: $subject\n\n"
            send "Email sent on $ts_date at $ts_time.\n"
            send "\n.\n"

            expect "250" {
                send "quit\n"
            }
          }
        }
      }
    }
  }
}
