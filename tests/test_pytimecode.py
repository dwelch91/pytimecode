"""Testing for pytimecode"""

import pytimecode
import unittest

class TestPyTimeCode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def debug(self, *s):
        pass

    def test_instan(self):
        timeobj = pytimecode.PyTimeCode('24', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('23.98', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('29.97', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('30', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('60', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('59.94', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('ms', '03:36:09:230')
        timeobj = pytimecode.PyTimeCode('ms', '03:36:09.230')
        timeobj = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)

    def test_repr_overload(self):
        timeobj = pytimecode.PyTimeCode('24', '01:00:00:00')
        self.assertEquals('01:00:00:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('23.98', '20:00:00:00')
        self.assertEquals('20:00:00:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('29.97', '00:09:00:00')
        self.assertEquals('00:09:00:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('30', '00:10:00:00')
        self.assertEquals('00:10:00:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('60', '00:00:09:00')
        self.assertEquals('00:00:09:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('59.94', '00:00:20:00')
        self.assertEquals('00:00:20:00', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('ms', '00:00:00:900')
        self.assertEquals('00:00:00.900', timeobj.__repr__())
        timeobj = pytimecode.PyTimeCode('24', start_timecode=None, frames=49)
        self.debug(timeobj.int_framerate)
        self.assertEquals('00:00:02:01', timeobj.__repr__())

    def test_timecode_init(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:00;01')
        self.assertEquals(1, tc.frames)
        tc = pytimecode.PyTimeCode('29.97', '03:36:09;23')
        self.assertEquals(388703, tc.frames)
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        self.assertEquals(389093, tc.frames)
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        self.assertEquals(389093, tc.frames)
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        self.assertEquals(324248, tc.frames)
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        self.assertEquals(778163, tc.frames)
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        self.assertEquals(778163, tc.frames)
        tc = pytimecode.PyTimeCode('59.94', '03:36:09;23')
        self.assertEquals(777383, tc.frames)
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        self.assertEquals(311279, tc.frames)
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        self.assertEquals(311279, tc.frames)
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(230, tc.frs)
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        self.assertEquals('00:08:20:00', tc.make_timecode())
        tc = pytimecode.PyTimeCode('29.97', start_timecode=None, frames=2589407, drop_frame=True)
        self.assertEquals('23:59:59;29', tc.make_timecode())
        tc = pytimecode.PyTimeCode('29.97', start_timecode=None, frames=2589408, drop_frame=True)
        self.assertEquals('00:00:00;00', tc.make_timecode())
        tc = pytimecode.PyTimeCode('59.94', start_timecode=None, frames=5178815, drop_frame=True)
        self.assertEquals('23:59:59;59', tc.make_timecode())
        tc = pytimecode.PyTimeCode('59.94', start_timecode=None, frames=5178816, drop_frame=True)
        self.assertEquals('00:00:00;00', tc.make_timecode())

    def test_frame_to_tc(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:00;01')
        tc.frames_to_tc()
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(0, tc.hrs)
        self.assertEquals(0, tc.mins)
        self.assertEquals(0, tc.secs)
        self.assertEquals(1, tc.frs)
        self.assertEquals('00:00:00;01', tc.make_timecode())

        tc = pytimecode.PyTimeCode('29.97', '03:36:09;23')
        tc.frames_to_tc()
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09;23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(23, tc.frs)

        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        tc.frames_to_tc()
        self.debug(tc.hrs, tc.mins, tc.secs, tc.frs)
        self.assertEquals(3, tc.hrs)
        self.assertEquals(36, tc.mins)
        self.assertEquals(9, tc.secs)
        self.assertEquals(230, tc.frs)

        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        self.assertEquals('00:08:20:00', tc.make_timecode())
        self.assertEquals(0, tc.hrs)
        self.assertEquals(8, tc.mins)
        self.assertEquals(20, tc.secs)
        self.assertEquals(0, tc.frs)

    def test_drop_frame(self):
        tc = pytimecode.PyTimeCode('59.94', '13:36:59;59')
        timecode = tc.next()
        self.assertEquals("13:37:00;04", timecode)

        tc = pytimecode.PyTimeCode('29.97', '13:36:59;29')
        timecode = tc.next()
        self.assertEquals("13:37:00;02", timecode)

        tc = pytimecode.PyTimeCode('59.94', '13:39:59;59')
        timecode = tc.next()
        self.assertEquals("13:40:00;00", timecode)

        tc = pytimecode.PyTimeCode('29.97', '13:39:59;29')
        timecode = tc.next()
        self.assertEquals("13:40:00;00", timecode)

    def test_iteration(self):
        tc = pytimecode.PyTimeCode('29.97', '03:36:09;23')  # 388703 fr
        # self.debug(tc.frames)
        for x in range(60):
            t = tc.next()
            assert t
        self.assertTrue(tc.drop_frame)
        self.assertEquals("03:36:11;23", t)  # 388767     (03:36:11;23 -> 388763 fr)
        self.assertEquals(388763, tc.frames)  # +4 fr

        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')  # 389093 fr
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:11:23", t)
        self.assertEquals(389153, tc.frames)

        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:11:23", t)
        self.assertEquals(389153, tc.frames)

        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:12:08", t)
        self.assertEquals(324308, tc.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:10:23", t)
        self.assertEquals(778223, tc.frames)

        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:10:23", t)
        self.assertEquals(778223, tc.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09;23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:10;23", t)
        self.assertEquals(777443, tc.frames)

        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:12:11", t)
        self.assertEquals(311339, tc.frames)

        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("03:36:12:11", t)
        self.assertEquals(311339, tc.frames)

        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals('03:36:09.290', t)
        self.assertEquals(12969290, tc.frames)

        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        for x in range(60):
            t = tc.next()
            assert t
        self.assertEquals("00:08:22:12", t)
        self.assertEquals(12060, tc.frames)

    def test_op_overloads_add(self):
        tc = pytimecode.PyTimeCode('29.97', '03:36:09;23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29;23')
        d = tc + tc2
        f = tc + 893
        self.debug(tc.frames, tc2.frames)
        self.assertEquals("03:36:39;16", d.make_timecode())
        self.assertEquals(389596, d.frames)
        self.assertEquals("03:36:39;16", f.make_timecode())
        self.assertEquals(389596, f.frames)

        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23')
        d = tc + tc2
        f = tc + 893
        self.assertEquals("03:36:39:16", d.make_timecode())
        self.assertEquals(389986, d.frames)
        self.assertEquals("03:36:39:16", f.make_timecode())
        self.assertEquals(389986, f.frames)

        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('30', '00:00:29:23')
        d = tc + tc2
        f = tc + 893
        self.assertEquals("03:36:39:16", d.make_timecode())
        self.assertEquals(389986, d.frames)
        self.assertEquals("03:36:39:16", f.make_timecode())
        self.assertEquals(389986, f.frames)

        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('25', '00:00:29:23')
        d = tc + tc2
        f = tc + 748
        self.assertEquals("03:36:39:21", d.make_timecode())
        self.assertEquals(324996, d.frames)
        self.assertEquals("03:36:39:21", f.make_timecode())
        self.assertEquals(324996, f.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23')
        d = tc + tc2
        f = tc + 1763
        self.assertEquals("03:36:38:46", d.make_timecode())
        self.assertEquals(779926, d.frames)
        self.assertEquals("03:36:38:46", f.make_timecode())
        self.assertEquals(779926, f.frames)

        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('60', '00:00:29:23')
        d = tc + tc2
        f = tc + 1763
        self.assertEquals("03:36:38:46", d.make_timecode())
        self.assertEquals(779926, d.frames)
        self.assertEquals("03:36:38:46", f.make_timecode())
        self.assertEquals(779926, f.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09;23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29;23')
        d = tc + tc2
        f = tc + 1763
        self.assertEquals("03:36:38;46", d.make_timecode())
        self.assertEquals(779146, d.frames)
        self.assertEquals("03:36:38;46", f.make_timecode())
        self.assertEquals(779146, f.frames)

        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc + tc2
        f = tc + 719
        self.assertEquals("03:36:39:22", d.make_timecode())
        self.assertEquals(311998, d.frames)
        self.assertEquals("03:36:39:22", f.make_timecode())
        self.assertEquals(311998, f.frames)

        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc + tc2
        f = tc + 719
        self.assertEquals("03:36:39:22", d.make_timecode())
        self.assertEquals(311998, d.frames)
        self.assertEquals("03:36:39:22", f.make_timecode())
        self.assertEquals(311998, f.frames)

        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        tc2 = pytimecode.PyTimeCode('ms', '01:06:09:230')
        d = tc + tc2
        f = tc + 719
        self.debug(tc.frames, tc2.frames, d.frames)
        self.assertEquals("04:42:18.460", d.make_timecode())
        self.assertEquals(16938460, d.frames)
        self.assertEquals("03:36:09.949", f.make_timecode())
        self.assertEquals(12969949, f.frames)

        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        tc2 = pytimecode.PyTimeCode('24', start_timecode=None, frames=485)
        d = tc + tc2
        f = tc + 719
        self.assertEquals("00:08:40:05", d.make_timecode())
        self.assertEquals(12485, d.frames)
        self.assertEquals("00:08:49:23", f.make_timecode())
        self.assertEquals(12719, f.frames)

    def test_op_overloads_mult(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:09;23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29;23')
        d = tc * tc2
        f = tc * 4
        self.debug(tc.frames, tc2.frames)
        self.assertEquals("02:25:30;11", d.make_timecode())
        self.assertEquals(261649, d.frames)
        self.assertEquals("00:00:39;02", f.make_timecode())
        self.assertEquals(1172, f.frames)

        tc = pytimecode.PyTimeCode('29.97', '00:00:09:23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23')
        d = tc * tc2
        f = tc * 4
        self.assertEquals("02:25:21:19", d.make_timecode())
        self.assertEquals(261649, d.frames)
        self.assertEquals("00:00:39:02", f.make_timecode())
        self.assertEquals(1172, f.frames)

        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('30', '00:00:29:23')
        d = tc * tc2
        f = tc * 893
        self.assertEquals("01:13:21:19", d.make_timecode())
        self.assertEquals(347460049, d.frames)
        self.assertEquals("01:13:21:19", f.make_timecode())
        self.assertEquals(347460049, f.frames)

        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('25', '00:00:29:23')
        d = tc * tc2
        f = tc * 748
        self.assertEquals("06:51:40:04", d.make_timecode())
        self.assertEquals(242537504, d.frames)
        self.assertEquals("06:51:40:04", f.make_timecode())
        self.assertEquals(242537504, f.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23')
        d = tc * tc2
        f = tc * 1763
        self.assertEquals("15:23:42:49", d.make_timecode())
        self.assertEquals(1371901369, d.frames)
        self.assertEquals("15:23:42:49", f.make_timecode())
        self.assertEquals(1371901369, f.frames)

        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('60', '00:00:29:23')
        d = tc * tc2
        f = tc * 1763
        self.assertEquals("15:23:42:49", d.make_timecode())
        self.assertEquals(1371901369, d.frames)
        self.assertEquals("15:23:42:49", f.make_timecode())
        self.assertEquals(1371901369, f.frames)

        tc = pytimecode.PyTimeCode('59.94', '03:36:09;23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29;23')
        d = tc * tc2
        f = tc * 1763
        self.assertEquals("15:22:48;45", d.make_timecode())
        self.assertEquals(1370526229, d.frames)
        self.assertEquals("15:22:48;45", f.make_timecode())
        self.assertEquals(1370526229, f.frames)

        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc * tc2
        f = tc * 719
        self.assertEquals("22:23:20:01", d.make_timecode())
        self.assertEquals(223809601, d.frames)
        self.assertEquals("22:23:20:01", f.make_timecode())
        self.assertEquals(223809601, f.frames)

        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc * tc2
        f = tc * 719
        self.assertEquals("22:23:20:01", d.make_timecode())
        self.assertEquals(223809601, d.frames)
        self.assertEquals("22:23:20:01", f.make_timecode())
        self.assertEquals(223809601, f.frames)

        # tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        # tc2 = pytimecode.PyTimeCode('ms', '01:06:09:230')
        # d = tc * tc2
        # f = tc * 719
        # self.debug(tc.frames, tc2.frames, d.frames)
        # self.assertEquals("12:39:52:900", d.make_timecode())
        # self.assertEquals(45592900, d.frames)
        # self.assertEquals("22:14:36:370", f.make_timecode())
        # self.assertEquals(80076370, f.frames)

        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        tc2 = pytimecode.PyTimeCode('24', start_timecode=None, frames=485)
        d = tc * tc2
        f = tc * 719
        self.assertEquals("19:21:40:00", d.make_timecode())
        self.assertEquals(5820000, d.frames)
        self.assertEquals("03:51:40:00", f.make_timecode())
        self.assertEquals(8628000, f.frames)

    # @unittest.skip
    def test_24_hour_limit(self):
        tc = pytimecode.PyTimeCode('24', '00:00:00:21')
        tc2 = pytimecode.PyTimeCode('24', '23:59:59:23')
        self.assertEquals('00:00:00:20', (tc + tc2).make_timecode())
        self.assertEquals('02:00:00:00', (tc2 + 159840001).make_timecode())

        tc = pytimecode.PyTimeCode('29.97', '00:00:00:21')
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59:29')
        self.debug((tc + tc2).frames)
        self.assertEquals('00:00:00:20', (tc + tc2).make_timecode())
        self.assertEquals('02:00:00:00', (tc2 + 18360001).make_timecode())

        tc = pytimecode.PyTimeCode('29.97', '00:00:00;01')
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59;29')
        tc3 = (tc2+21)
        self.debug('yp1', tc.frames, tc2.frames, tc3.frames, tc.make_timecode())
        self.assertEquals('00:00:00;20',  tc3.make_timecode())

        tc = pytimecode.PyTimeCode('29.97', '00:00:00;21')
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59;29')
        tc3 = (tc+tc2)
        self.debug('yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode())
        self.assertEquals('00:00:00;20',  tc3.make_timecode())

        tc = pytimecode.PyTimeCode('29.97', '04:20:13;21')
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59;29')
        tc3 = (tc+tc2)
        self.debug('yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode())
        self.assertEquals('04:20:13;20',  tc3.make_timecode())

        tc = pytimecode.PyTimeCode('59.94', '04:20:13;21')
        tc2 = pytimecode.PyTimeCode('59.94', '23:59:59;59')
        tc3 = (tc+tc2)
        self.debug('yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode())
        self.assertEquals('04:20:13;20',  tc3.make_timecode())

    def test_case_1(self):
        start = pytimecode.PyTimeCode('29.97', "01:00:00;00")
        self.assertEquals(start.frames, 107892)

        end = pytimecode.PyTimeCode('29.97', "01:01:00;02")
        self.assertEquals(end.frames, 109692)

        diff = end - start
        self.assertEquals(diff.frames, 1800)  # 1800
        self.assertEquals(diff.make_timecode(), "00:01:00;02")   # 00:00:59;28

        end.add_frames(10)
        self.assertEquals(end.make_timecode(), "01:01:00;12")
        self.assertEquals(end.frames, 109702)  # 109700?

        start.sub_frames(10)
        self.assertEquals(start.make_timecode(), "00:59:59;20")
        self.assertEquals(start.frames, 107882)

        diff2 = end - start
        self.assertEquals(diff2.frames, 1820)
        self.assertEquals(diff2.make_timecode(), "00:01:00;22")

    # def test_case_2(self):
    #     pass
    #     tc = pytimecode.PyTimeCode('ms', '00:00:01:500')
    #     self.assertEquals(tc.frames, 1500)
    #     tc.convert_fps('29.97', True)
    #     #self.assertEquals(tc.make_timecode(), "00:00:01;15")
    #     self.assertEquals(tc.frames, 1500)
    #     self.assertEquals(tc.make_timecode(), "00:03:25;06")
    #
    #
    #     tc2 = pytimecode.PyTimeCode('29.97', '00:01:01;01')
    #     tc2.convert_fps('60', False)
    #     # self.assertEquals(tc2.make_timecode(), '00:01:01:02')
    #     self.assertEquals(tc2.make_timecode(), '00:00:30:29')

    def test_exceptions(self):
        e = None
        try:
            tc = pytimecode.PyTimeCode('24', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('23.98', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('29.97', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('30', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('60', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('59.94', '01:20:30:303')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:303'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('ms', '01:20:30:3039')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals("Timecode string parsing error: '01:20:30:3039'", e.__str__())

        try:
            tc = pytimecode.PyTimeCode('60', '01:20:30;30')
        except ValueError as e:
            self.debug(type(e), e)
            self.assertEquals('Drop frame with 60fps not supported, only 29.97 & 59.94.', e.__str__())

        tc = pytimecode.PyTimeCode('29.97', '00:00:09;23')
        tc2 = 'bum'
        try:
            d = tc * tc2
        except ValueError as e:
            self.assertEquals("Type <class 'str'> not supported for arithmetic.", e.__str__())

        tc = pytimecode.PyTimeCode('30', '00:00:09:23')
        tc2 = 'bum'
        try:
            d = tc + tc2
        except ValueError as e:
            self.assertEquals("Type <class 'str'> not supported for arithmetic.", e.__str__())

        tc = pytimecode.PyTimeCode('24', '00:00:09:23')
        tc2 = 'bum'
        try:
            d = tc - tc2
        except ValueError as e:
            self.assertEquals("Type <class 'str'> not supported for arithmetic.", e.__str__())

        tc = pytimecode.PyTimeCode('ms', '00:00:09:237')
        tc2 = 'bum'
        try:
            d = tc / tc2
        except (TypeError, ValueError) as e:
            self.assertEquals("unsupported operand type(s) for /: 'PyTimeCode' and 'str'", e.__str__())

