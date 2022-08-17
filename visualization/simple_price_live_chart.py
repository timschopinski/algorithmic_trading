from datetime import datetime
import time
from typing import List
import matplotlib.pyplot as plt
import matplotlib


class SimpleLiveChart:
    """
        SimpleChart enables collecting price and volume data and displaying
        as a chart or saving as png image by passing
        display=True and save=True as **kwargs
    """

    def __init__(self, number_of_plots: int = 1, *args, **kwargs):
        assert 1 <= number_of_plots <= 3, 'numbers_of_plots must be higher than 0 and lower than 4!'
        self.number_of_plots = number_of_plots
        self._data = [
            {f'plot{i}': {
                'values': [],
                'title': kwargs.get(f'title{i+1}', None),
                'x_label': kwargs.get(f'x_label{i+1}', None),
                'y_label': kwargs.get(f'y_label{i+1}', None),
                'background_color': kwargs.get(f'background_color{i+1}', 'lightgreen'),
            }} for i in range(number_of_plots)
        ]
        self._markers = []
        self.is_displaying_chart = kwargs.get('display', True)
        self.is_saving_to_file = kwargs.get('save', True)
        self.plot = None
        if self.is_saving_to_file:
            file_path = kwargs.get('file_path', None)
            if file_path is None:
                raise ValueError('If save=True you have to provide a file_path!')
            else:
                assert isinstance(file_path, str), 'You have to provide a valid file_path'
                self.file_path = file_path
        if kwargs.get('window', False):
            matplotlib.use('TkAgg')  # Your favorite interactive or non-interactive backend

    def add_value(self, plot_number: int, value: float):
        self._data[plot_number][f'plot{plot_number}']['values'].append(value)

    def set_labels(self, axs):
        if self.number_of_plots == 1:
            axs.set_title(self._data[0][f'plot0']['title'])
            axs.set_xlabel(self._data[0][f'plot0']['x_label'])
            axs.set_ylabel(self._data[0][f'plot0']['y_label'])
            return
        for i in range(self.number_of_plots):
            axs[i].set_title(self._data[i][f'plot{i}']['title'])
            axs[i].set_xlabel(self._data[i][f'plot{i}']['x_label'])
            axs[i].set_ylabel(self._data[i][f'plot{i}']['y_label'])

    def add_marker(self, plot_number: int, value: float, marker_type: str):

        if marker_type == 'BUY':
            marker_type = 'g^'
        elif marker_type == 'SELL':
            marker_type = 'rv'

        self._markers.append(
            {
                'plot_number': plot_number,
                'x_value': len(self._data[plot_number][f'plot{plot_number}']['values']) - 1,
                'y_value': value,
                'marker_type': marker_type,
            }
        )

    def plot_values(self, axs):
        if self.number_of_plots == 1:
            axs.plot(self._data[0][f'plot0']['values'])
            return
        [axs[i].plot(self._data[i][f'plot{i}']['values']) for i in range(self.number_of_plots)]

    def plot_markers(self, axs):
        if not self._markers:
            return
        if self.number_of_plots == 1:
            for marker in self._markers:
                axs.plot(marker['x_value'], marker['y_value'], marker.get('marker_type', 'bo'))
            return
        for marker in self._markers:
            plot_number = marker['plot_number']
            axs[plot_number].plot(marker['x_value'], marker['y_value'], marker.get('marker_type', 'bo'))
        return

    def display_chart(self):
        fig, axs = plt.subplots(self.number_of_plots)
        self.set_background_color(axs)
        self.plot_values(axs)
        self.plot_markers(axs)
        self.set_labels(axs)
        plt.show()
        plt.close(fig)

    def set_background_color(self, axs):
            if self.number_of_plots == 1:
                axs.set_facecolor(self._data[0][f'plot{0}']['background_color'])
                return
            for i in range(self.number_of_plots):
                axs[i].set_facecolor(self._data[i][f'plot{i}']['background_color'])

    def save_to_file(self):
        fig, axs = plt.subplots(self.number_of_plots)
        self.set_background_color(axs)
        self.plot_values(axs)
        self.plot_markers(axs)
        self.set_labels(axs)
        plt.savefig(self.file_path)
        plt.close(fig)

    def render(self):
        if self.is_displaying_chart:
            self.display_chart()
        if self.is_saving_to_file:
            self.save_to_file()


def main():
    # matplotlib.use('TkAgg')  # Your favorite interactive or non-interactive backend

    s = SimpleLiveChart(
        number_of_plots=2,
        title1='BTCUSDT',
        # title2='Volume',
        # x_label1='Time [s]',
        x_label2='Time [s]',
        y_label1='Price [USDT]',
        y_label2='Volume',
        background_color1='grey',
        background_color2='blue',
        file_path='test/test.png'
    )
    s.add_value(0, 12)
    s.add_value(0, 15)
    s.add_value(0, 8)
    s.add_value(1, 12)
    s.add_value(1, 9)
    s.add_value(1, 5)
    s.add_marker(0, 10, 'SELL')
    s.render()
    s.render()
    #
    # x_values = [datetime(2021, 11, 18, 12), datetime(2021, 11, 18, 14), datetime(2021, 11, 18, 16)]
    # y_values = [1.0, 3.0, 2.0]
    #
    # dates = matplotlib.dates.date2num(x_values)
    # matplotlib.pyplot.plot_date(dates, y_values)
    # plt.show()

    # s.add_value(12)
    # s.render()


if __name__ == '__main__':
    main()