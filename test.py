#!/usr/bin/env python3

from unittest import main, TestCase, mock
from io import StringIO

from timertool import _timer

class TestTimerClass(TestCase):

    def setUp(self):
        self.timer = mock.MagicMock(spec=_timer._timer)

    def test_constructor(self):
        timer = _timer._timer()
        self.assertIsNone(timer._time)

    @mock.patch('time.time')
    def test_start(self, mock_time):
        _timer._timer.start(self.timer)
        self.assertEqual(self.timer._start_time, mock_time.return_value)

    def test_stop(self):
        result = _timer._timer.stop(self.timer)
        self.assertEqual(result, self.timer._get_time.return_value)
        self.assertEqual(self.timer._time, self.timer._get_time.return_value)

    def test_enter(self):
        result = _timer._timer.__enter__(self.timer)
        self.assertEqual(result, self.timer)
        self.timer.start.assert_called_with()

    def test_exit(self):
        _timer._timer.__exit__(self.timer, 0, 0, 0)
        self.timer.stop.assert_called_with()

    @mock.patch('time.time', return_value=10)
    def test_get_time(self, mock_time):
        self.timer._start_time = 3
        result = _timer._timer._get_time(self.timer)
        self.assertEqual(result, 7)
        mock_time.assert_called_with()

    def test_time_property_not_done(self):
        self.timer._time = None
        result = _timer._timer.time.fget(self.timer)
        self.assertEqual(result, self.timer._get_time.return_value)
        self.timer._get_time.assert_called_with()

    def test_time_property_done(self):
        self.timer._time = 1
        result = _timer._timer.time.fget(self.timer)
        self.assertEqual(result, self.timer._time)
        self.timer._get_time.assert_not_called()


class TestTimerFunc(TestCase):

    @mock.patch.object(_timer, '_timer')
    def test_timer(self, mock_timer):
        self.assertEqual(_timer.timer(), mock_timer.return_value)
        mock_timer.assert_called_with()


class TestTimerIntegration(TestCase):

    @mock.patch('time.time')
    def test_enter_start(self, mock_time):
        timer = _timer._timer()
        with timer as t:
            self.assertEqual(t, timer)
            self.assertEqual(timer._start_time, mock_time.return_value)

    @mock.patch('time.time', return_value=10)
    def test_stop_get_time(self, mock_time):
        timer = _timer._timer()
        timer._start_time = 2
        result = timer.stop()
        self.assertEqual(result, 8)
        self.assertEqual(timer._time, 8)

    @mock.patch('time.time', return_value=10)
    def test_exit_stop(self, mock_time):
        timer = _timer._timer()
        with timer as t:
            timer._start_time = 2
        self.assertEqual(timer._time, 8)

    @mock.patch('time.time', side_effect=[4, 10])
    def test_enter_exit(self, mock_time):
        timer = _timer._timer()
        with timer:
            pass
        self.assertEqual(timer._time, 6)

    @mock.patch('time.time', side_effect=[4, 10, 20])
    def test_time_property(self, mock_time):
        timer = _timer._timer()
        with timer as t:
            self.assertEqual(timer.time, 6)
        self.assertEqual(timer.time, 16)

    @mock.patch('time.time', side_effect=[4, 10, 20])
    def test_start_stop(self, mock_time):
        timer = _timer._timer()
        timer.start()
        self.assertEqual(timer.time, 6)
        timer.stop()
        self.assertEqual(timer.time, 16)

    @mock.patch('time.time', side_effect=[4, 10, 20])
    def test_timer_function_start_stop(self, mock_time):
        timer = _timer.timer()
        timer.start()
        self.assertEqual(timer.time, 6)
        timer.stop()
        self.assertEqual(timer.time, 16)

    @mock.patch('time.time', side_effect=[4, 10, 20])
    def test_timer_function_with_statement(self, mock_time):
        with _timer.timer() as t:
            self.assertEqual(t.time, 6)
        self.assertEqual(t.time, 16)


class TestTimerlog(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('time.time', side_effect=[15, 18])
    def test_decorator(self, mock_time, mock_stdout):
        mock_func = mock.MagicMock(__name__='foo')
        decorated_func = _timer.timelog(mock_func)
        result = decorated_func('foo', bar='baz')
        mock_func.assert_called_with('foo', bar='baz')
        self.assertEqual(result, mock_func.return_value)
        self.assertEqual("foo: 3 sec\n", mock_stdout.getvalue())


if __name__ == "__main__":
    main()
