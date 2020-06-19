

class CollisionDetector:

    def __init__(self, sample=None):
        self.sample = sample

    def processSamples(self):
        '''
        Procesa una muestra o caso de prueba
        Esta funcion es la entrada de todo el proceso
        '''

        return self.checkObjectsDistance(self.sample)

    def checkObjectsDistance(self, sample=None):
        '''
        Compara 2 bounding boxes por iteracion.
        Este proceso se divide en dos operaciones [verifyCollision y checkXYobjsDistances]
        '''
        if sample is None:
            return None

        collision_detected = False

        for i in range(len(sample)):
            for j in range(i, len(sample)):
                if list(sample[i])[-1] != list(sample[j])[-1]:
                    collision_detected = self.verifyCollision(
                        [sample[i], sample[j]])
                    if collision_detected:
                        return collision_detected

        return False

    def checkObjMaxArea(self, maxArea, objs):
        #print(maxArea)

        for obj in objs:
            if maxArea in obj:
                if obj[-1] == 'forklift':
                    return (0.5 * maxArea) #/ 100
                return (0.3 * maxArea) #/ 100

    def verifyCollision(self, bb_results=None):
        '''
        se sacan las areas de cada bounding box del set pasado por parametro.
        estas areas se comparan para revisar si sus dimensiones son compatibles ( 1:1 )
        una vez hecho este proceso se regresa Falso en no ser compatibles y en caso contrario,
        se pasan los datos al siguiente proceso [checkXYobjsDistances]
        '''
        obj_area_1 = list(bb_results[0])[0]
        obj_area_2 = list(bb_results[1])[0]
        # print(bb_results[0])
        # Revisa si ambos objetos tienen la misma escala (se encuentran en la misma posicion de x o y)
        #print(
            #f'AREA 1: {obj_area_1} {bb_results[0][-1]}, AREA 2: {obj_area_2} {bb_results[1][-1]}')

        max_area = max(obj_area_1, obj_area_2)
        min_area = min(obj_area_1, obj_area_2)
        if max_area == min_area or (max_area - (max_area * self.checkObjMaxArea(max_area, bb_results)) < min_area):
            xy1 = (list(bb_results[0])[1], list(
                bb_results[0])[2], list(bb_results[0])[3], list(
                bb_results[0])[4])
            xy2 = (list(bb_results[1])[1], list(bb_results[1])[2], list(bb_results[1])[3], list(
                bb_results[1])[4])
            xyclose = self.checkXYobjsDistances(xy1=xy1, xy2=xy2)
            if xyclose:
                #print(
                    #f'AREA 1: {obj_area_1} {bb_results[0][-1]}, AREA 2: {obj_area_2} {bb_results[1][-1]}')
                return True

        return False

    def checkObjMinXY(self, minXY, objs):
        print(minXY)

        for obj in objs:
            if minXY in obj:
                if obj[-1] == 'forklift':
                    return (0.5 * minXY)  # / 100
                return (0.3 * minXY)  # / 100

    def checkXYobjsDistances(self, xy1=None, xy2=None):
        '''
        Se revisa que las coordenadas de ambas bounding boxes esten cercanas y no alejadas en algun eje.
        Regresa True en el caso donde ambas bounding boxes esten cerca tanto en X como en Y
        Regresa False en caso contrario
        '''
        xy1 = list(xy1)
        xy2 = list(xy2)

        lower_x_1 = xy1[0]
        upper_y_1 = xy1[1]
        lower_x_2 = xy2[0]
        upper_y_2 = xy2[1]

        max_x = max(lower_x_1, lower_x_2)
        min_x = min(lower_x_1, lower_x_2)

        max_y = max(upper_y_1, upper_y_2)
        min_y = min(upper_y_1, upper_y_2)

        max_x_data = xy1 if max_x in xy1 else xy2
        max_y_data = xy1 if max_y in xy1 else xy2

        min_x_data = xy1 if min_x in xy1 else xy2
        min_y_data = xy1 if min_y in xy1 else xy2

        is_x_close = False
        is_y_close = False

        is_x_close = (min_x + max_x_data[2] >
                      max_x) or ((min_x + min_x_data[2] + ((min_x + min_x_data[2]) * .10) > max_x))

        is_y_close = (min_y + max_y_data[3] >
                      max_y) or ((min_y + min_y_data[3] + ((min_y + min_y_data[3]) * .05)) > max_y)

        #print(f'WIDTH: montacargas : {xy2[2]}')

        # print(f'{is_x_close} and {is_y_close}')

        # print('\n', xy1, xy2, end='\n')

        # print(f'are bounding boxes close in x {is_x_close}, y {is_y_close} \n')

        return is_x_close and is_y_close
