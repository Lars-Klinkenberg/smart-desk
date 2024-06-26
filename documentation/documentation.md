# Software used
QElectroTech - creating circuit diagram

# Pinout
| Network cable | Desk cable | Function |
| --- | --- | --- |
| Orange | Red | ? |
| Orange White | Yellow | + 35V |
| Green | Yellow | + 5V |
| Green White | White | RX |
| Brown | Brown | Ground |
| Brown White | Black | TX |
| Blue | Lila | Ground |
| Blue White  | - |  |

# Serial Data
**Idle Data:**

 ['a5', '00', '00', 'ff', 'ff’]

a5 ⇒ Start bit

00 ⇒ data

00 ⇒ data

ff ⇒ data

ff ⇒ end bit

**write TX down**

[ 'a5', '00', '10', 'ef', 'ff’]

a5 ⇒ Start bit

00 ⇒ data

10 ⇒ data

ef ⇒ data

ff ⇒ end bit

**write TX up**

['a5', '00', '02', 'fd', 'ff’]

a5 ⇒ Start bit

00 ⇒ data

02 ⇒ data

fd ⇒ data

ff ⇒ end bit