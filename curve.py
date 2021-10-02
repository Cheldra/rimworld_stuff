def post_process_curve(pre, x=[0, 5, 40, 10000], y=[0, 14, 40, 10000]):
    for i in range(len(x)):
        if pre < x[i]:
            gradient =  (y[i] - y[i - 1])/(x[i] - x[i - 1])
            progress = pre - x[i - 1]
            return y[i - 1] + gradient*progress


def area_under_line(x, y):
    rectangle_area = (x[1] - x[0])*min(y)
    triangle_area = 0.5*(x[1] - x[0])*(max(y) - min(y))
    return rectangle_area + triangle_area


def expected_from_discrete_curve(x=[0.5, 1, 1.5, 2], y=[0, 1, 1, 0]):
    total_volume = 0
    total_area = 0
    for i in range(len(x) - 1):
        current_x = x[i]
        current_y = y[i]
        current_interger = round(current_x)
        next_interger_boundary = current_interger + 0.5
        while True:
            if next_interger_boundary < x[i + 1]:
                y_at_boundary = post_process_curve(next_interger_boundary, x=x, y=y)
                area = area_under_line([current_x, next_interger_boundary], [current_y, y_at_boundary])
                total_volume += area*current_interger
                total_area += area
                
                current_y = y_at_boundary
                current_x = next_interger_boundary
                current_interger += 1
                next_interger_boundary += 1
            else:
                area = area_under_line([current_x, x[i + 1]], [current_y, y[i + 1]])
                total_volume += area*current_interger
                total_area += area
                break
        
    return total_volume/total_area

class rat:
    def __init__(self):
        self.x = [0.5, 1, 2.2, 2.8]
        self.y = [0, 1, 1, 0]

if __name__ == '__main__':
    target = rat()
    print(post_process_curve(140*0.04))
    print(expected_from_discrete_curve(target.x, target.y))

    
