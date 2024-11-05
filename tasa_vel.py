from manim import *
import numpy as np

class VelocidadConfig:
    # Tiempos de espera iniciales
    WAIT_BEFORE_START = 31  # "Cuando ustedes van en auto"
    
    # Tiempos para la secuencia del velocímetro
    SPEEDOMETER_START = 38  # "Digamos que el velocímetro"
    NEEDLE_ROTATION_DURATION = 2  # Duración de la rotación
    
    # Tiempos para las demostraciones de distancia
    DISTANCE_DEMOS = {
        'HOUR_1': 48,
        'HOUR_0_5': 51,
        'HOUR_0_25': 54
    }
    
    # Duración de cada demostración
    DEMO_DURATION = 2
    
    # Tiempo final para la notación
    NOTATION_TIME = 67  # "Se puede escribir kilómetros por hora"
    
    # Duraciones de las animaciones
    CREATION_DURATION = 1
    CAR_MOVEMENT_DURATION = 2
    RETURN_DURATION = 1

class VelocidadComoTasa(Scene):
    def construct(self):
        # Configuración inicial
        road = Rectangle(height=0.5, width=14, color=GRAY)
        road.shift(DOWN * 2)
        
        # Crear el auto usando formas básicas
        car = VGroup()
        body = Rectangle(height=1, width=2, fill_opacity=1, color=BLUE)
        wheel1 = Circle(radius=0.2, fill_opacity=1, color=WHITE)
        wheel2 = Circle(radius=0.2, fill_opacity=1, color=WHITE)
        wheel1.next_to(body, DOWN, buff=0)
        wheel2.next_to(body, DOWN, buff=0)
        wheel1.shift(LEFT * 0.5)
        wheel2.shift(RIGHT * 0.5)
        car.add(body, wheel1, wheel2)
        car.scale(0.7)
        car.move_to(road.get_left() + RIGHT * 2 + UP * 0.5)
        
        # Crear el velocímetro
        speedometer = Circle(radius=1.5, color=WHITE)
        speedometer.shift(UP * 2 + RIGHT * 4)
        speeds = [0, 20, 40, 60, 80, 100]
        angle_range = 240  # grados
        labels = VGroup()
        
        for i, speed in enumerate(speeds):
            angle = -180 + (i * angle_range / (len(speeds) - 1))
            angle_rad = np.deg2rad(angle)
            label_pos = speedometer.get_center() + 1.8 * np.array([
                np.cos(angle_rad),
                np.sin(angle_rad),
                0
            ])
            label = Text(str(speed), font_size=20)
            label.move_to(label_pos)
            labels.add(label)
        
        # Aguja del velocímetro
        needle = Line(
            speedometer.get_center(),
            speedometer.get_center() + UP * 1.3,
            color=RED
        )
        
        # Textos explicativos
        title = Text("Velocidad como Tasa", font_size=40)
        title.to_edge(UP)
        
        explanation = Text(
            "60 km/h significa:",
            font_size=30
        ).next_to(speedometer, LEFT, buff=3)
        
        # Esperar hasta el inicio de la explicación
        self.wait(VelocidadConfig.WAIT_BEFORE_START)
        
        # Crear elementos base con timing controlado
        self.play(
            Create(road),
            FadeIn(car),
            Create(speedometer),
            Create(labels),
            Create(needle),
            Write(title),
            run_time=VelocidadConfig.CREATION_DURATION
        )
        
        # Esperar hasta el momento de la rotación
        self.wait(VelocidadConfig.SPEEDOMETER_START - VelocidadConfig.WAIT_BEFORE_START - VelocidadConfig.CREATION_DURATION)
        
        # Rotar aguja
        self.play(
            Rotate(
                needle,
                angle=230 * DEGREES,
                about_point=speedometer.get_center()
            ),
            run_time=VelocidadConfig.NEEDLE_ROTATION_DURATION
        )
        
        self.play(Write(explanation))
        
        # Demostraciones de distancia
        times = [1, 0.5, 0.25]
        start_times = [
            VelocidadConfig.DISTANCE_DEMOS['HOUR_1'],
            VelocidadConfig.DISTANCE_DEMOS['HOUR_0_5'],
            VelocidadConfig.DISTANCE_DEMOS['HOUR_0_25']
        ]
        
        for i, (time, start_time) in enumerate(zip(times, start_times)):
            # Esperar hasta el momento correcto
            if i == 0:
                self.wait(start_time - VelocidadConfig.SPEEDOMETER_START - VelocidadConfig.NEEDLE_ROTATION_DURATION)
            else:
                self.wait(start_time - start_times[i-1] - VelocidadConfig.DEMO_DURATION)
            
            distance = int(60 * time)
            distance_text = Text(
                f"En {time} hora{'s' if time != 1 else ''}: {distance} km",
                font_size=25
            ).next_to(explanation, DOWN * (i + 2))
            
            marker = Line(UP, DOWN, color=YELLOW).next_to(
                road.get_left() + RIGHT * (2 + distance * 0.2),
                UP,
                buff=0
            )
            marker_label = Text(f"{distance}km", font_size=20).next_to(marker, UP)
            
            # Animación de la demostración
            self.play(
                Write(distance_text),
                Create(marker),
                Write(marker_label),
                car.animate.move_to(
                    road.get_left() + RIGHT * (2 + distance * 0.2) + UP * 0.5
                ),
                run_time=VelocidadConfig.DEMO_DURATION
            )
            
            # Regresar el auto si no es la última demostración
            if i < len(times) - 1:
                self.play(
                    car.animate.move_to(road.get_left() + RIGHT * 2 + UP * 0.5),
                    run_time=VelocidadConfig.RETURN_DURATION
                )
        
        # Esperar hasta el tiempo de notación
        self.wait(VelocidadConfig.NOTATION_TIME - VelocidadConfig.DISTANCE_DEMOS['HOUR_0_25'] - VelocidadConfig.DEMO_DURATION)

# Ejecutar la animación
if __name__ == '__main__':
    scene = VelocidadComoTasa()
    scene.render()