"""Module for manipulating SMPTE timecode. Supports 60, 59.94, 50, 30, 29.97, 25, 24, 23.98 frame rates in drop and
non-drop where applicable, and milliseconds. It also supports
operator overloading for addition, subtraction, multiplication, and division.

iter_return sets the format that iterations return, the options are "tc" for a timecode string,
"frames" for a int total frames, and "tc_tuple" for a tuple of ints in the following format,
(hours, minutes, seconds, frames).

Notes: *There is a 24 hour SMPTE Timecode limit, so if your time exceeds that limit, it will roll over.
       *2 PyTimeCode objects of the same frame rate is the only supported way to combine PyTimeCode objects,
            for example adding them together.

Copyright Joshua Banton"""


# heavily modified from original 0.1.0 version in PyPi to fix defects


class PyTimeCode(object):
    def __init__(self, framerate, start_timecode=None, frames=None, drop_frame=False, iter_return="tc"):
        """frame rate can be string '60', '59.94', '50', '30', '29.97', '25', '24', '23.98', or 'ms'"""
        self.framerate = framerate
        self.int_framerate = self.set_int_framerate()
        self.drop_frame = drop_frame
        if start_timecode and drop_frame and len(start_timecode) > 8 and start_timecode[8] != ';':
            raise ValueError("If drop_frame is True and a start timecode is specified, the tc must use drop frame format.")
        self.iter_return = iter_return
        self.hrs = None
        self.mins = None
        self.secs = None
        self.frs = None
        self.frames = None
        if start_timecode:
            self.set_timecode(start_timecode)
            self.tc_to_frames()
        elif frames is not None:  # because 0==False, and frames can be 0
            self.frames = int(frames)
            if self.frames < 0:
                self.frames = 0
            self.frames_to_tc()
        self.__check_drop_frame__()

    def set_timecode(self, timecode):
        """sets timecode to argument 'timecode'"""
        self.hrs, self.mins, self.secs, self.frs, self.drop_frame = self.parse_timecode(timecode)

    def total_seconds(self):
        drop_fix = 0

        if self.drop_frame:
            drop_fix = 2 * (self.mins % 10)

            if self.framerate == '59.94':
                drop_fix *= 2

        return (self.hrs * 3600) + (self.mins * 60) + self.secs + (self.frames - drop_fix) / self.int_framerate

    def tc_to_frames(self):
        """converts corrent timecode to frames"""
        total_mins = 60 * self.hrs + self.mins
        frames = (((total_mins * 60) + self.secs) * self.int_framerate) + self.frs
        if self.drop_frame:
            frames -= (2 if self.framerate == '29.97' else 4) * (total_mins - (total_mins // 10))
        self.frames = frames

    def frames_to_tc(self):
        """converts frames back to timecode
        """
        if self.drop_frame:
            drop_frames = self.calc_drop_frames()
            frames = self.frames + drop_frames
        else:
            frames = self.frames
        self.hrs = frames // (3600 * self.int_framerate)
        # check to see if hours => 24. SMPTE Timecode only goes to 24 hours
        if self.hrs > 23:
            self.hrs %= 24
            frames -= 24 * 3600 * self.int_framerate

        self.mins = (frames % (3600 * self.int_framerate)) // (60 * self.int_framerate)
        self.secs = ((frames % (3600 * self.int_framerate)) % (60 * self.int_framerate)) // self.int_framerate
        self.frs = ((frames % (3600 * self.int_framerate)) % (60 * self.int_framerate)) % self.int_framerate

    def calc_drop_frames(self):
        # 'formula' taken from http://www.andrewduncan.ws/Timecodes/Timecodes.html
        #if self.framerate not in ('29.97', '59.94'):
        if not self.drop_frame:
            return 0

        drop_frames_per_event = 2
        frames_per_10min = 17982
        frames_per_min_for_min_1_9 = 1798
        if self.framerate == '59.94':
            drop_frames_per_event *= 2
            frames_per_10min *= 2
            frames_per_min_for_min_1_9 *= 2

        ten_min_segs = self.frames // frames_per_10min
        extra_frames = self.frames % frames_per_10min
        extra_minutes_beyond_minute_0 = \
            ((extra_frames - drop_frames_per_event) // frames_per_min_for_min_1_9) if \
            extra_frames > drop_frames_per_event else 0

        return drop_frames_per_event * ((9 * ten_min_segs) + extra_minutes_beyond_minute_0)

    def set_int_framerate(self):
        if self.framerate == '29.97':
            int_framerate = 30
        elif self.framerate == '59.94':
            int_framerate = 60
        elif self.framerate == '23.98':
            int_framerate = 24
        elif self.framerate == 'ms':
            int_framerate = 1000
        elif self.framerate == 'frames':
            int_framerate = 1
        else:
            int_framerate = int(self.framerate)
        return int_framerate

    def parse_timecode(self, timecode):
        """parses timecode string frames '00:00:00:00' or '00:00:00;00' or milliseconds '00:00:00:000'"""
        if len(timecode) == 11:
            frs = int(timecode[9:11])
            drop = timecode[8] == ';'
        elif len(timecode) == 12 and self.framerate == 'ms':
            frs = int(timecode[9:12])
            drop = False
        else:
            raise ValueError('Timecode string parsing error. ' + timecode)

        hrs = int(timecode[0:2])
        mins = int(timecode[3:5])
        secs = int(timecode[6:8])
        return hrs, mins, secs, frs, drop

    def make_timecode(self):
        self.frames_to_tc()
        hr_str = self.__set_time_str(self.hrs)
        min_str = self.__set_time_str(self.mins)
        sec_str = self.__set_time_str(self.secs)
        frame_str = self.__set_time_str(self.frs)
        drop_char = ':'
        if self.framerate == 'ms':
            drop_char = '.'
        elif self.drop_frame:
            drop_char = ';'
        timecode_str = "%s:%s:%s%s%s" % (hr_str, min_str, sec_str, drop_char, frame_str)
        return timecode_str

    def __set_time_str(self, time):
        return str(int(time)).zfill(2)

    def __iter__(self):
        return self

    def next(self):
        self.add_frames(1)
        return self.__return_item__()

    def back(self):
        self.sub_frames(1)
        return self.__return_item__()

    def __check_drop_frame__(self):
        if not self.drop_frame:
            return True
        elif self.framerate == "29.97" or self.framerate == "59.94":
            return True
        else:
            raise ValueError('Drop frame with ' + self.framerate + 'fps not supported, only 29.97 & 59.94.')

    def __return_item__(self):
        if self.iter_return == 'tc':
            return self.make_timecode()
        elif self.iter_return == 'frames':
            return self.frames
        elif self.iter_return == 'tc_tuple':
            self.make_timecode()
            return self.hrs, self.mins, self.secs, self.frs

    def add_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames + frames

    def sub_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames - frames
        if self.frames < 0:
            self.frames = 0

    def mult_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames * frames

    def div_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames // frames

    def __add__(self, other):
        """returns new pytimecode object with added timecodes"""
        if isinstance(other, PyTimeCode):
            added_frames = self.frames + other.frames
        elif type(other) == int:
            added_frames = self.frames + other
        else:
            raise ValueError('Type ' + str(type(other)) + ' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, frames=added_frames, drop_frame=self.drop_frame)
        return newtc

    def __sub__(self, other):
        """returns new pytimecode object with added timecodes"""
        if isinstance(other, PyTimeCode):
            subtracted_frames = self.frames - other.frames
        elif type(other) == int:
            subtracted_frames = self.frames - other
        else:
            raise ValueError('Type ' + str(type(other)) + ' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, frames=subtracted_frames, drop_frame=self.drop_frame)
        return newtc

    def __mul__(self, other):
        """returns new pytimecode object with added timecodes"""
        if isinstance(other, PyTimeCode):
            mult_frames = self.frames * other.frames
        elif type(other) == int:
            mult_frames = self.frames * other
        else:
            raise ValueError('Type ' + str(type(other)) + ' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, frames=mult_frames, drop_frame=self.drop_frame)
        return newtc

    def __div__(self, other):
        """returns new pytimecode object with added timecodes"""
        if isinstance(other, PyTimeCode):
            div_frames = self.frames // other.frames
        elif type(other) == int:
            div_frames = self.frames // other
        else:
            raise ValueError('Type ' + str(type(other)) + ' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, frames=div_frames, drop_frame=self.drop_frame)
        return newtc

    def __repr__(self):
        return self.make_timecode()


