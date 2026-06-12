import time
import machine
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from machine import Pin, I2C
from machine import ADC, Pin
import bme280

vsys = ADC(29)                      # reads the system input voltage
charging = Pin(24, Pin.IN)          # reading WL_GPIO2 tells us whether or not USB power is connected
conversion_factor = 3 * 3.3 / 65535

full_battery = 4.3                  # these are our reference voltages for a full/empty battery, in volts
empty_battery = 3.0                 # the values could vary by b

i2c=I2C(0,sda=Pin(8), scl=Pin(9), freq=400000)    #initializing the I2C method

# Buttons
button_a = machine.Pin(12, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_c = machine.Pin(14, machine.Pin.IN, pull=machine.Pin.PULL_UP)

# Display
display = PicoGraphics(display=DISPLAY_INKY_PACK) #296x128
#WIDTH, HEIGHT = display.get_bounds()
display.set_update_speed(2)
#graphics.set_font("gothic")

t_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
h_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
p_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
d_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dmin = 0
dmax = 0
def clear():
    display.set_pen(15)
    display.clear()

def kiir():
    clear()
    display.set_pen(0)
    display.set_font("bitmap8")
       
    if b==1 :
        tmin = 100
        tmax = 0
        display.set_pen(0)
        for i in range(1, 42):				#minimum keresés
            if t_list[i-1] < tmin:
                tmin = t_list[i-1]
            #else:
             #   tmin = t_list[i]
                
        for i in range(1, 42):				#maximun keresés
            if tmax < t_list[i-1]:
                tmax = t_list[i-1]
        dmin=tmin
        dmax=tmax    
        tmin=int(tmin-1)
        tmax=int(tmax+1)
          
        for i in range(1, 42):
            d_list[i-1] = ((t_list[i-1]-tmin)/(tmax-tmin))*100
            
        display.text("  "+str(tmax), 0, 26, 240, 2)
        display.text("  °C", 0, 58, 240, 2)
        display.text("  "+str(tmin), 0, 93, 240, 2)
        
    if b==2 :
        hmin = 100
        hmax = 0
        display.set_pen(0)
        display.text("   %", 0, 78, 240, 2)
        display.text("  50", 0, 58, 240, 2)
        display.text("  75", 0, 42, 240, 2)
        display.text(" 100", 0, 26, 240, 2)
        
        for i in range(1, 42):				#minimum keresés
            if h_list[i-1] < hmin:
                hmin = h_list[i-1]
            #else:
             #   tmin = t_list[i]
                
        for i in range(1, 42):				#maximun keresés
            if hmax < h_list[i-1]:
                hmax = h_list[i-1]
                
        dmin=hmin
        dmax=hmax
        
        for i in range(1, 42):
            d_list[i-1] = h_list[i-1]
            
    if b==3 :
        display.set_pen(0)
        pmin = 2000
        pmax = 0
        
        for i in range(1, 42):					#minimum keresés
            if p_list[i-1] < pmin:
                pmin = p_list[i-1]
                
        for i in range(1, 42):					#maximun keresés
            if pmax < p_list[i-1]:
                pmax = p_list[i-1]
        dmin=pmin
        dmax=pmax    
        pmin=int(pmin-1)
        pmax=int(pmax+1)
        
        
        for i in range(1, 42):
            d_list[i-1] = ((p_list[i-1]-pmin)/(pmax-pmin))*100
            
        display.text(str(pmax), 0, 26, 240, 2)		# a skála kiírása
        display.text("hPa", 0, 58, 240, 2)
        display.text(str(pmin), 0, 93, 240, 2)
        
    
    display.text(str(t_list[40])+ "°C", 0, 0, 240, 3)
    display.text(str(int(h_list[40]))+ "%", 110, 0, 240, 3)
    display.text(str(int(p_list[40]))+"hPa", 180, 0, 240, 3)
    display.text("    min: "+str(dmin)+"  max: "+str(dmax), 44, 110, 240, 2)

    display.line(40, 30, 40, 128 , 2)
    display.line(35, 100, 296, 100 , 2)
    #display.line(35, 82, 45, 82 , 2)    #25%
    #display.line(35, 65, 45, 65 , 2)    #50%
    #display.line(35, 47, 45, 47 , 2)    #75%
    display.line(35, 30, 45, 30 , 2)    #100%
        
    for i in range(1, 42):
      m=int(d_list[i-1]*0.7)
      #print (m)
      #display.rectangle(40+(i-1)*23, 100-m, 23, m)  # display.rectangle(x, y, w, h)
      display.line(40+(i-1)*6, 100-m, 40+i*6, 100-m, 2)
   
    if charging.value() == 1:         # if it's plugged into USB power...
#        print("Charging!")
        display.text("Tölt", 0, 110, 240, 2)
    else:                             # if not, display the battery stats
#        print(voltage)
#        print(percentage)
        voltageout = str(voltage)[:4]
        display.text(voltageout, 0, 110, 240, 2)
        #display.text(str(voltage), 0, 110, 240, 2)
   
    display.update()

def button(pin):
    global b
    if pin == button_a:
       b=1
    if pin == button_b:
       b=2
    if pin == button_c:
       b=3
    kiir()
    return
            

button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)
button_c.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)

clear()
b=3
bme = bme280.BME280(i2c=i2c)        #BME280 object created
temperature = bme.values[0]         #reading the value of temperature
pressure = bme.values[1]            #reading the value of pressure
humidity = bme.values[2]            #reading the value of humidity
time.sleep(1)
temperature = bme.values[0]         #reading the value of temperature
pressure = bme.values[1]            #reading the value of pressure
humidity = bme.values[2]            #reading the value of humidity

t = temperature.replace("C", "")
h = humidity.replace("%", "")
p = pressure.replace("hPa", "")
for i in range(1, 42):
            t_list[i-1] = float(t)
            h_list[i-1] = float(h)
            p_list[i-1] = float(p)

while True:
    bme = bme280.BME280(i2c=i2c)        #BME280 object created
    temperature = bme.values[0]         #reading the value of temperature
    pressure = bme.values[1]            #reading the value of pressure
    humidity = bme.values[2]            #reading the value of humidity

    del t_list[0]
#    print (temperature)
    t = temperature.replace("C", "")
#    print (t_list)
    t_list.append(float(t))
    
    del h_list[0]
#    print (humidity)
    h = humidity.replace("%", "")
#    print (h)
    h_list.append(float (h))
    
    del p_list[0]
#    print (pressure)
    p = pressure.replace("hPa", "")
    p_list.append(float (p))
#    print (p)

    voltage = vsys.read_u16() * conversion_factor
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100.00

    # add text


    kiir()
    
    time.sleep(10)