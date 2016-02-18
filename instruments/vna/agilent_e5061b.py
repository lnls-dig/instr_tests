# define specific class for Agilent E5061B Network Analyzer

import visa

class AgilentE5061B:
    """Class used to send commands and acquire data from the Agilent E5061B vector network analyzer.
    """



    def __init__(self, rm,  ip):
        """Class constructor. Here the socket connection to the instrument is initialized. The
        argument required, a string, is the IP adress of the instrument."""

        vna_ip = ip

        self.vna_socket = rm.open_resource('TCPIP::' + vna_ip + '::inst0::INSTR')

        #self.vna_socket.send(b":SYST:PRES\n")
        #self.vna_socket.send(b":DISP:WIND1:TRAC1:Y:RLEV -40\n")
        #self.vna_socket.send(b":DISP:WIND1:TRAC1:Y:PDIV 15\n")
        #self.vna_socket.send(b":SENS1:SWE:TIME:AUTO ON\n")
        #self.vna_socket.send(b":SENS1:SWE:POIN 1601\n")
        #self.vna_socket.send(b":SENS1:SWE:TYPE LIN\n")
        #self.vna_socket.send(b":SOUR1:POW:GPP 0.0\n")

        self.vna_socket.write(":SYST:PRES")
        self.vna_socket.write(":DISP:WIND1:TRAC1:Y:RLEV -40")
        self.vna_socket.write(":DISP:WIND1:TRAC1:Y:PDIV 15")
        self.vna_socket.write(":SENS1:SWE:TIME:AUTO ON")
        self.vna_socket.write(":SENS1:SWE:POIN 1601")
        self.vna_socket.write(":SENS1:SWE:TYPE LIN")
        self.vna_socket.write(":SOUR1:POW:GPP 0.0")


    def query(self, text):
        """Return the output of the query on text"""
        return self.vna_socket.query(text)

    def write(self, text):
        """Sends a command to the instrument."""
        self.vna_socket.write(text)
        #time.sleep(SLEEP_TIME)
        return

    def get_frequency_data(self):
        """Get the list of frequencies of the instrument sweep, returning a sequence of floating
           point numbers."""
        frequency_data = self.vna_socket.query(":SENS1:FREQ:DATA?")
        frequency_data = frequency_data[:len(frequency_data) - 1].split(",")
        frequency_data = [float(i) for i in frequency_data]
        return(frequency_data)

    def get_s11_data(self):
        """Get the S11 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S11")
        #time.sleep(SLEEP_TIME)
        s11_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s11_data = s11_data[:len(s11_data) - 1].split(",")
        s11_data = s11_data[::2]
        s11_data = [round(float(i),2) for i in s11_data]
        return(s11_data)

    def get_s12_data(self):
        """Get the S12 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S12")
        #time.sleep(SLEEP_TIME)
        s12_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s12_data = s12_data[:len(s12_data) - 1].split(",")
        s12_data = s12_data[::2]
        s12_data = [round(float(i),2) for i in s12_data]
        return(s12_data)

    def get_s21_data(self):
        """Get the S21 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S21")
        #time.sleep(SLEEP_TIME)
        s21_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s21_data = s21_data[:len(s21_data) - 1].split(",")
        s21_data = s21_data[::2]
        s21_data = [round(float(i),2) for i in s21_data]
        return(s21_data)

    def get_s22_data(self):
        """Get the S22 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.write(":CALC1:PAR1:DEF S22")
        #time.sleep(SLEEP_TIME)
        s22_data = self.vna_socket.query(":CALC1:DATA:FDAT?")
        s22_data = s22_data[:len(s22_data) - 1].split(",")
        s22_data = s22_data[::2]
        s22_data = [round(float(i),2) for i in s22_data]
        return(s22_data)

    def set_marker_frequency(self,value):
        """set the center frequency of the VNA"""
        self.vna_socket.write(":CALC1:MARK1:X " + str(value))

    def get_marker_value(self,marker):
        """get the value of the marker 1 """
        #self.vna_socket.write(":CALC1:MARK" + str(marker) + ":Y?")
        #ans= self.vna_socket.read_raw()
        ans = self.vna_socket.query(":CALC1:MARK" + str(marker) + ":Y?")
        index = ans.find(',')
        ans = ans[:index].strip()
        return(ans)

    def set_center_frequency(self, freq):
        """set the center frequency of the VNA"""
        self.vna_socket.write(":SENS1:FREQ:CENT " + str(freq))
        return

    def set_span(self,freq):
        """set the span of the VNA"""
        self.vna_socket.write(":SENS1:FREQ:SPAN " + str(freq))
        return

    def set_power(self, power):
        self.vna_socket.write(":SOUR1:POW:GPP " + str(power))
        return

    #def close_connection(self):
    #    """Close the socket connection to the instrument."""
    #    self.vna_socket.close()
