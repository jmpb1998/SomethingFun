import as7262

as7262.soft_reset()
as7262.set_gain(64)
as7262.set_integration_time(17.857)
as7262.set_measurement_mode(2)
as7262.set_illumination_led(1)

totred = 0
totorange = 0
totyellow = 0
totgreen = 0
totblue = 0
totviolet = 0

try:
    for i in range(50):
        values = as7262.get_calibrated_values()
        print("""
Red:    {}
Orange: {}
Yellow: {}
Green:  {}
Blue:   {}
Violet: {}""".format(*values))
        totred += values.red
        totorange += values.orange
        totyellow += values.yellow
        totgreen += values.green
        totblue += values.blue
        totviolet += values.violet
    
    totred = totred/50
    totorange = totorange/50
    totyellow = totyellow/50
    totgreen = totgreen/50
    totblue = totblue/50
    totviolet = totviolet/50    



except KeyboardInterrupt:
    as7262.set_measurement_mode(3)
    as7262.set_illumination_led(0)
