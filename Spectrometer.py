"""
This program is designed to open communications with the Jaz Spectrometer. 
"""


import seabreeze.spectrometers as sb

           
def initalizeOceanOptics():
    global spec
    spec = sb.Spectrometer.from_serial_number()
    return spec
    
def setIntegrationTime(time = 1000000):
    
    #time = Intgration time in microseconds, default is 1 s
    #spec is the spectrometer object
    
    spec.integration_time_micros(time)
    
def getWavelength():
    wavelength = spec.wavelengths()
    return wavelength

def getIntensity():
    intensity = spec.intensities()
    return intensity

def closeSpectrometer():
    spec.close()



