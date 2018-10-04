# SY-Harmony-Selenium-Python-Automator
Workforce Management Software: SY-HARMONY : http://www.synel.com/harmony-workforce-management/

This is a Python script in order to fill the work hours every day automatically in Sy-Harmony, using Selenium.

In order to make this working, there are few things that need to be done:

* Create an entry in Credential Manager to store password that will be used:
** Service Name: eHarmony
** Username: <eHarmony Username>
** Password: <eHarmony Password>
* Change harmony_url to the right one.

Then, you just need to run the following command:
```sh
$ python harmonyAutomator.py <username> <Start Work XX:XX> <End Work XX:XX> <Execute in Background 0-No 1-Yes>
```

<username> - Required

<Start Work XX:XX> - Optional, Default 09:00

<End Work XX:XX> - Optional, Default 18:00

<Execute in Background 0-No 1-Yes> - Optional, Default 0
