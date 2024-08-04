# smart-desk
This is a personal project to control my standing desk using a Raspberry Pi 4. The setup is specifically tailored to my hardware and requirements, and is not intended for general customization. However, feel free to use it if you find it helpful.

## Features

- Height Adjustment: Automatically adjusts the height of the desk.
- Preset Heights: Save and recall preset desk heights.
- User-Friendly Interface: Control the desk through a web interface.

## Hardware information
- motor controller id - Wp-cb01
- Desk interface circuit board id - Dcu_g-PRT5G

# Setup information
- Serial Ports on the Raspberry must be enabled

## libs
`pip instll pyserial`
`pip install flask`
`pip install flask-classful`
`pip install rpi.gpio`
`pip install python-dotenv`
`pip install mariadb`