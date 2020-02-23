from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys
from typing import List
from math import sqrt
from decimal import Decimal
import random
import csv

SQUARE_SIZE = (35, 35)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, settings, show=True, fps=200):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor(240, 240, 240))
        self.setPalette(palette)
        self.settings = settings

        # Determine size of next gen based off selection type
        self._next_gen_size = None
        if 'plus':
            self._next_gen_size = 1500
        elif self.settings['selection_type'].lower() == 'comma':
            self._next_gen_size = self.settings['num_offspring']
        else:
            raise Exception('Selection type "{}" is invalid'.format(self.settings['selection_type']))

        
        self.board_size = (10, 10)
        self.border = (0, 10, 0, 10)  # Left, Top, Right, Bottom
        self.snake_widget_width = SQUARE_SIZE[0] * self.board_size[0]
        self.snake_widget_height = SQUARE_SIZE[1] * self.board_size[1]

        # Allows padding of the other elements even if we need to restrict the size of the play area
        self._snake_widget_width = max(self.snake_widget_width, 620)
        self._snake_widget_height = max(self.snake_widget_height, 600)

        self.top = 150
        self.left = 150
        self.width = self._snake_widget_width + 700 + self.border[0] + self.border[2]
        self.height = self._snake_widget_height + self.border[1] + self.border[3] + 200

        self.best_fitness = 0
        self.best_score = 0

        self._current_individual = 0



        self.current_generation = 0

        self.init_window()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000./fps)

        if show:
            self.show()

    def init_window(self):
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Snake AI')
        self.setGeometry(self.top, self.left, self.width, self.height)





        # Genetic Algorithm Stats window
        self.ga_window = GeneticAlgoWidget(self.centralWidget, self.settings)
        self.ga_window.setGeometry(QtCore.QRect(200, self.border[1] + self.border[3] + self.snake_widget_height, self._snake_widget_width + self.border[0] + self.border[2] + 100, 200-10))
        self.ga_window.setObjectName('ga_window')




class GeneticAlgoWidget(QtWidgets.QWidget):
    def __init__(self, parent, settings):
        super().__init__(parent)

        font = QtGui.QFont('Times', 11, QtGui.QFont.Normal)
        font_bold = QtGui.QFont('Times', 11, QtGui.QFont.Bold)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setColumnStretch(1, 5)
        TOP_LEFT = Qt.AlignLeft | Qt.AlignTop

        LABEL_COL = 0
        STATS_COL = 1
        ROW = 0

        #### Generation stuff ####
        # Generation
        self._create_label_widget_in_grid('Generation: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self.current_generation_label = self._create_label_widget('1', font)
        grid.addWidget(self.current_generation_label, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Current individual
        self._create_label_widget_in_grid('Individual: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self.current_individual_label = 'qqqqqqq'
        #grid.addWidget(self.current_individual_label, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Best score
        self._create_label_widget_in_grid('Best Score: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self.best_score_label = self._create_label_widget('0', font)
        #grid.addWidget(self.best_score_label, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Best fitness
        self._create_label_widget_in_grid('Best Fitness: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self.best_fitness_label = self._create_label_widget('{:.2E}'.format(Decimal('0.1')), font)
        #grid.addWidget(self.best_fitness_label, ROW, STATS_COL, TOP_LEFT)

        ROW = 0
        LABEL_COL, STATS_COL = LABEL_COL + 2, STATS_COL + 2

        #### GA setting ####
        self._create_label_widget_in_grid('GA Settings', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        ROW += 1

        # Selection type
        selection_type = 'vvvvv'
        self._create_label_widget_in_grid('Selection Type: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(selection_type, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Crossover type
        crossover_type = 'wwwwww'
        self._create_label_widget_in_grid('Crossover Type: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(crossover_type, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Mutation type
        mutation_type = 'xxxxx'
        self._create_label_widget_in_grid('Mutation Type: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(mutation_type, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Mutation rate
        self._create_label_widget_in_grid('Mutation Rate:', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        mutation_rate = 'yyyyy'
        self._create_label_widget_in_grid(mutation_rate, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Lifespan
        self._create_label_widget_in_grid('Lifespan: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        lifespan = 'zzzzz'
        self._create_label_widget_in_grid(lifespan, font, grid, ROW, STATS_COL, TOP_LEFT)

        ROW = 0
        LABEL_COL, STATS_COL = LABEL_COL + 2, STATS_COL + 2

        #### NN setting ####
        self._create_label_widget_in_grid('NN Settings', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        ROW += 1

        # Hidden layer activation
        hidden_layer_activation = 'NNNNNNN'
        self._create_label_widget_in_grid('Hidden Activation: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(hidden_layer_activation, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Output layer activation
        output_layer_activation = 'OOOOOOO'
        self._create_label_widget_in_grid('Output Activation: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(output_layer_activation, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Network architecture
        network_architecture = 'PPPPPP'
        self._create_label_widget_in_grid('NN Architecture: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(network_architecture, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Snake vision
        snake_vision = 'QQQQQQQQQ"'
        self._create_label_widget_in_grid('Snake Vision: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        self._create_label_widget_in_grid(snake_vision, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        # Snake/Apple vision type
        self._create_label_widget_in_grid('Apple/Self Vision: ', font_bold, grid, ROW, LABEL_COL, TOP_LEFT)
        apple_self_vision_type = 'RRRRRRRRR'
        self._create_label_widget_in_grid(apple_self_vision_type, font, grid, ROW, STATS_COL, TOP_LEFT)
        ROW += 1

        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(5, 2)

        self.setLayout(grid)

        self.show()

    def _create_label_widget(self, string_label: str, font: QtGui.QFont) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel()
        label.setText(string_label)
        label.setFont(font)
        label.setContentsMargins(0,0,0,0)
        return label

    def _create_label_widget_in_grid(self, string_label: str, font: QtGui.QFont, 
                                     grid: QtWidgets.QGridLayout, row: int, col: int, 
                                     alignment: Qt.Alignment) -> None:
        label = QtWidgets.QLabel()
        label.setText(string_label)
        label.setFont(font)
        label.setContentsMargins(0,0,0,0)
        grid.addWidget(label, row, col, alignment)






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(None)
    sys.exit(app.exec_())