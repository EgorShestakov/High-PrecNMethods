import matplotlib.pyplot as plt


def plot_settings(ax, t, exact, approx, label, color_exact, color_approx, title, ylabel):
    """
    Настройка и построение графика на заданной оси
    """
    ax.plot(t, exact, label=f'Точное решение {label}',
        color=color_exact, linestyle='-')
    ax.plot(t, approx, label=f'Приближённое решение {label}',
        color=color_approx, linestyle='--')
    ax.set_title(title)
    ax.set_xlabel('Время (t)')
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()


def build_option_graph(x, y, x_approx, y_approx, t, h, method_name):
    plt.figure(figsize=(12, 5))

    # Общий заголовок для всего рисунка
    plt.suptitle(f'Решение задачи методом {method_name} с шагом h = {h}', fontsize=14, fontweight='bold')

    ax1 = plt.subplot(1, 2, 1)
    plot_settings(ax1, t, x, x_approx, 'X', 'blue', 'red',
        'График для X', 'Значение X')

    ax2 = plt.subplot(1, 2, 2)
    plot_settings(ax2, t, y, y_approx, 'Y', 'blue', 'red',
        'График для Y', 'Значение Y')

    plt.tight_layout()
    plt.show()
