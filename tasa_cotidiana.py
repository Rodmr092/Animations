from manim import *
import numpy as np

class AnimationConfig:
    # Tiempos iniciales
    INITIAL_WAIT = 1  # "Detén el video y piensa..."
    
    # Tiempos para el mercado
    MARKET_START = 15  # "Vamos a ver un ejemplo..."
    WEIGHING_TIMES = {
        'FIRST': 26,   # "Digamos que llevas..."
        'SECOND': 34,  # "1 kilo..."
        'THIRD': 37,   # "2 kilos..."
        'CONCLUSION': 67  # "Lo más correcto sería..."
    }
    
    # Tiempos para la cocina
    KITCHEN_START = 76  # "Pasemos a la cocina..."
    RECIPE_TIMES = {
        'FIRST_RATIO': 83,  # "Ocupo un huevo..."
        'SECOND_RATIO': 88  # "Por cada huevo ocupo..."
    }
    
    # Tiempos para deportes
    SPORTS_START = 106  # "En los deportes..."
    GOALS_TIMES = {
        'FIRST_GAME': 123,  # "En el primer partido..."
        'SECOND_GAME': 127, # "En el segundo..."
        'THIRD_GAME': 129,  # "En el tercero..."
        'CALCULATION': 136  # "Para obtener la tasa..."
    }
    
    # Duraciones de las animaciones
    ICON_CREATION_DURATION = 1
    ZOOM_DURATION = 2
    TRANSITION_DURATION = 1.5
    WEIGHING_DURATION = 1
    TABLE_CREATION_DURATION = 0.3
    BALL_CREATION_DURATION = 0.3

class DigitalScale(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Crear la base de la balanza
        self.base = RoundedRectangle(
            height=3,
            width=4,
            corner_radius=0.2,
            fill_color=GREY_A,
            fill_opacity=1,
            stroke_color=GREY_D
        )
        
        # Crear la pantalla LCD
        self.screen = RoundedRectangle(
            height=1,
            width=2.5,
            corner_radius=0.1,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_D
        ).next_to(self.base.get_top(), DOWN, buff=0.2)
        
        # Textos en la pantalla
        self.weight_display = Text("0.000 kg", font_size=24, color=GREEN)
        self.price_display = Text("$0.00", font_size=24, color=RED)
        self.weight_display.next_to(self.screen.get_top(), DOWN, buff=0.1)
        self.price_display.next_to(self.weight_display, DOWN, buff=0.1)
        
        # Plataforma para las zanahorias
        self.platform = Rectangle(
            height=1.5,
            width=3,
            fill_color=GREY_C,
            fill_opacity=1,
            stroke_color=GREY_D
        ).next_to(self.screen, DOWN, buff=0.2)
        
        # Agregar todos los componentes
        self.add(self.base, self.screen, self.weight_display, self.price_display, self.platform)
    
    def update_display(self, weight_kg, price):
        new_weight = Text(f"{weight_kg:.3f} kg", font_size=24, color=GREEN)
        new_price = Text(f"${price:.2f}", font_size=24, color=RED)
        
        new_weight.move_to(self.weight_display.get_center())
        new_price.move_to(self.price_display.get_center())
        
        return AnimationGroup(
            Transform(self.weight_display, new_weight),
            Transform(self.price_display, new_price)
        )

class TasasCotidianas(Scene):
    def create_carrot(self, scale_factor=0.3):
        # Crear una zanahoria simplificada usando formas básicas
        carrot = VGroup()
        
        # Cuerpo de la zanahoria (triángulo naranja)
        body = Triangle(fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE)
        body.rotate(PI)  # Voltear el triángulo
        body.scale(scale_factor)
        
        # Hojas (triángulos verdes)
        leaves = VGroup()
        for angle in [-30, 0, 30]:
            leaf = Triangle(fill_color=GREEN, fill_opacity=1, stroke_color=GREEN)
            leaf.scale(scale_factor * 0.4)
            leaf.rotate(angle * DEGREES)
            leaf.next_to(body.get_top(), UP, buff=0)
            leaves.add(leaf)
        
        carrot.add(body, leaves)
        return carrot

    def create_market_scene(self):
        # Título
        price_explanation = Text(
            "Comparemos precios por kilogramo",
            font_size=36
        ).to_edge(UP)
        
        # Crear balanza
        scale = DigitalScale().scale(0.8).shift(DOWN)
        
        # Crear grupos de zanahorias
        carrot_groups = VGroup()
        positions = []
        
        # Configurar posiciones para las zanahorias
        base_pos = scale.platform.get_center() + UP * 0.2
        for row in range(2):
            for col in range(4):
                positions.append(base_pos + RIGHT * (col - 1.5) * 0.4 + UP * (row - 0.5) * 0.4)
        
        # Crear grupos de zanahorias (2, 4 y 8 zanahorias)
        for num_carrots in [2, 4, 8]:
            group = VGroup()
            for i in range(num_carrots):
                carrot = self.create_carrot()
                carrot.move_to(positions[i])
                group.add(carrot)
            carrot_groups.add(group)
        
        market_scene = VGroup(price_explanation, scale)
        market_scene.carrot_groups = carrot_groups
        
        return market_scene

    def show_kitchen_scene(self):
        # Título
        recipe_title = Text("Receta de Hot Cakes", font_size=36).to_edge(UP)
        
        # Íconos de ingredientes
        ingredients = VGroup()
        egg = SVGMobject("assets/egg.svg").scale(0.3)
        milk = SVGMobject("assets/milk.svg").scale(0.3)
        ingredients.add(egg, milk)
        ingredients.arrange(RIGHT, buff=1)
        ingredients.next_to(recipe_title, DOWN, buff=0.3)
        
        # Crear tabla
        headers = ["Huevos", "Tazas de leche", "Proporción"]
        data = [["1", "2", "1:2"],
                ["2", "4", "1:2"],
                ["3", "6", "1:2"]]
        
        table = Table([headers] + data, include_outer_lines=True).scale(0.8)
        table.next_to(ingredients, DOWN, buff=0.5)
        table_elements = VGroup()
        
        # Mostrar elementos básicos
        self.play(
            Write(recipe_title),
            FadeIn(ingredients),
            run_time=AnimationConfig.TABLE_CREATION_DURATION
        )
        
        # Esperar hasta el primer ratio
        self.wait(AnimationConfig.RECIPE_TIMES['FIRST_RATIO'] - AnimationConfig.KITCHEN_START - AnimationConfig.TABLE_CREATION_DURATION)
        
        # Animar la tabla fila por fila
        for i, row in enumerate([headers] + data):
            for j, cell_content in enumerate(row):
                cell = table.get_cell((i+1, j+1))
                cell_text = table.get_entries((i+1, j+1))
                table_elements.add(cell, cell_text)
                self.play(
                    Create(cell),
                    Write(cell_text),
                    run_time=AnimationConfig.TABLE_CREATION_DURATION
                )
        
        # Esperar hasta el segundo ratio
        self.wait(AnimationConfig.RECIPE_TIMES['SECOND_RATIO'] - AnimationConfig.RECIPE_TIMES['FIRST_RATIO'])
        
        # Mostrar las dos formas de escribir la tasa
        rate1 = Text("1:2", font_size=36, color=BLUE)
        rate2 = Text("1 huevo por 2 tazas de leche", font_size=36, color=BLUE)
        
        rate1.next_to(table, DOWN, buff=0.5)
        rate2.next_to(rate1, DOWN, buff=0.3)
        
        self.play(Write(rate1))
        self.play(Write(rate2))
        
        kitchen_scene = VGroup(recipe_title, ingredients, table_elements, rate1, rate2)
        
        # Esperar hasta la escena de deportes
        self.wait(AnimationConfig.SPORTS_START - AnimationConfig.RECIPE_TIMES['SECOND_RATIO'])
        
        return kitchen_scene

    def show_sports_scene(self):
        # Título
        stats_title = Text("Goles por Partido", font_size=36).to_edge(UP)
        
        # Tabla inicial
        stats_table = Table(
            [["Partido", "Goles"],
             ["1", ""],
             ["2", ""],
             ["3", ""]],
            include_outer_lines=True
        ).scale(0.8)
        stats_table.next_to(stats_title, DOWN, buff=0.5)
        
        # Datos para animar
        goles_por_partido = [2, 3, 4]
        soccer_balls = VGroup()
        
        # Mostrar título y tabla inicial
        self.play(
            FadeIn(stats_title),
            Create(stats_table),
            run_time=AnimationConfig.TABLE_CREATION_DURATION
        )
        
        # Esperar hasta el primer juego
        self.wait(AnimationConfig.GOALS_TIMES['FIRST_GAME'] - AnimationConfig.SPORTS_START)
        
        # Posición inicial para los balones
        ball_start_y = stats_table.get_bottom()[1] - 1
        accumulated_balls = 0
        
        # Animar cada fila y sus balones
        game_times = [
            AnimationConfig.GOALS_TIMES['FIRST_GAME'],
            AnimationConfig.GOALS_TIMES['SECOND_GAME'],
            AnimationConfig.GOALS_TIMES['THIRD_GAME']
        ]
        
        for i, (goles, start_time) in enumerate(zip(goles_por_partido, game_times)):
            if i > 0:
                self.wait(start_time - game_times[i-1] - AnimationConfig.BALL_CREATION_DURATION)
                
            # Actualizar la tabla
            new_cell = Text(str(goles), font_size=24)
            cell = stats_table.get_cell((i+2, 2))
            new_cell.move_to(cell)
            self.play(Write(new_cell))
            
            # Crear y animar los balones
            for j in range(goles):
                ball = SVGMobject("assets/soccer_ball.svg").scale(0.2)
                ball_x = -3 + (accumulated_balls + j) * 0.6
                ball.move_to(np.array([ball_x, ball_start_y, 0]))
                soccer_balls.add(ball)
                self.play(
                    FadeIn(ball),
                    run_time=AnimationConfig.BALL_CREATION_DURATION
                )
            
            accumulated_balls += goles
        
        # Esperar hasta el cálculo final
        self.wait(AnimationConfig.GOALS_TIMES['CALCULATION'] - AnimationConfig.GOALS_TIMES['THIRD_GAME'])
        
        # Agregar líneas divisorias para visualizar la división
        dividing_lines = VGroup()
        line_positions = [3, 6]  # Posiciones después del tercer y sexto balón
        for ball_count in line_positions:
            x_pos = -3 + (ball_count * 0.6) - 0.3  # Restamos la mitad del espaciado
            line = Line(
                start=np.array([x_pos, ball_start_y + 0.2, 0]),
                end=np.array([x_pos, ball_start_y - 0.2, 0]),
                color=YELLOW
            )
            dividing_lines.add(line)
        
        self.play(Create(dividing_lines))
        
        # Mostrar el cálculo de la tasa promedio
        calc_text = Text("9 goles ÷ 3 partidos = ", font_size=30).next_to(soccer_balls, DOWN, buff=0.5)
        final_rate = Text("3 goles/partido", font_size=30, color=BLUE).next_to(calc_text, RIGHT)
        
        self.play(
            Write(calc_text),
            Write(final_rate)
        )
        
        return VGroup(stats_title, stats_table, soccer_balls, dividing_lines, calc_text, final_rate)

    def construct(self):
        # Configuración de colores
        self.camera.background_color = BLACK
        
        # Crear íconos principales usando SVGs
        market_icon = SVGMobject("assets/supermarket.svg").scale(0.8)
        market_label = Text("Supermercado", font_size=24).next_to(market_icon, DOWN)
        market_group = VGroup(market_icon, market_label)
        
        kitchen_icon = SVGMobject("assets/kitchen.svg").scale(0.8)
        kitchen_label = Text("Cocina", font_size=24).next_to(kitchen_icon, DOWN)
        kitchen_group = VGroup(kitchen_icon, kitchen_label)
        
        sports_icon = SVGMobject("assets/sports.svg").scale(0.8)
        sports_label = Text("Deportes", font_size=24).next_to(sports_icon, DOWN)
        sports_group = VGroup(sports_icon, sports_label)
        
        # Posicionar íconos
        icons = VGroup(market_group, kitchen_group, sports_group).arrange(RIGHT, buff=2)
        original_market_position = market_group.get_center()
        original_kitchen_position = kitchen_group.get_center()
        original_sports_position = sports_group.get_center()
        
        # Esperar tiempo inicial
        self.wait(AnimationConfig.INITIAL_WAIT)
        
        # Animación inicial
        self.play(
            *[Create(icon) for icon in icons],
            run_time=AnimationConfig.ICON_CREATION_DURATION
        )
        
        # Esperar hasta la escena del mercado
        self.wait(AnimationConfig.MARKET_START - AnimationConfig.INITIAL_WAIT - AnimationConfig.ICON_CREATION_DURATION)
        
        # Escena Supermercado
        market_scene = self.create_market_scene()
        
        self.play(
            market_group.animate.scale(2).move_to(ORIGIN),
            FadeOut(kitchen_group),
            FadeOut(sports_group),
            run_time=AnimationConfig.ZOOM_DURATION
        )
        
        self.play(
            FadeOut(market_group),
            FadeIn(market_scene),
            run_time=AnimationConfig.TRANSITION_DURATION
        )
        
        # Mostrar la animación de la balanza
        scale = market_scene[1]
                
        # Esperar hasta el primer pesaje
        self.wait(AnimationConfig.WEIGHING_TIMES['FIRST'] - AnimationConfig.MARKET_START - AnimationConfig.ZOOM_DURATION - AnimationConfig.TRANSITION_DURATION)

        # Mostrar secuencia de pesaje
        weights = [0.5, 1.0, 2.0]  # en kg
        price_per_kg = 30
        weigh_times = [
            AnimationConfig.WEIGHING_TIMES['FIRST'],
            AnimationConfig.WEIGHING_TIMES['SECOND'],
            AnimationConfig.WEIGHING_TIMES['THIRD']
        ]

        for i, (weight, start_time) in enumerate(zip(weights, weigh_times)):
            if i > 0:
                # Esperamos el tiempo hasta la siguiente medición
                self.wait(start_time - weigh_times[i-1] - AnimationConfig.WEIGHING_DURATION)
                # Transicionamos directamente al siguiente grupo de zanahorias
                self.play(
                    FadeOut(market_scene.carrot_groups[i-1]),
                    FadeIn(market_scene.carrot_groups[i]),
                    scale.update_display(weight, weight * price_per_kg),
                    run_time=AnimationConfig.WEIGHING_DURATION
                )
            else:
                # Primera aparición de zanahorias
                self.play(
                    FadeIn(market_scene.carrot_groups[i]),
                    scale.update_display(weight, weight * price_per_kg),
                    run_time=AnimationConfig.WEIGHING_DURATION
                )

        # Esperar hasta la conclusión del mercado
        self.wait(AnimationConfig.WEIGHING_TIMES['CONCLUSION'] - AnimationConfig.WEIGHING_TIMES['THIRD'] - AnimationConfig.WEIGHING_DURATION)
        
        # Mostrar las dos formas de escribir la tasa
        rate1 = Text("30 pesos/kilo", font_size=36, color=BLUE)
        rate2 = Text("30 pesos por kilo", font_size=36, color=BLUE)
        
        rate1.next_to(scale, DOWN, buff=0.5)
        rate2.next_to(rate1, DOWN, buff=0.3)
        
        self.play(Write(rate1))
        self.play(Write(rate2))
        
        # Agregar una espera de 4 segundos antes de la transición
        self.wait(4)


        # Transición a vista general después del mercado
        self.play(
            FadeOut(market_scene),
            FadeOut(market_scene.carrot_groups),  
            FadeOut(rate1),
            FadeOut(rate2),
            FadeIn(kitchen_group),
            FadeIn(sports_group),
            FadeIn(market_group.scale(0.5).move_to(original_market_position)),
            run_time=AnimationConfig.TRANSITION_DURATION
        )
        
        # Escena Cocina
        self.play(
            kitchen_group.animate.scale(2).move_to(ORIGIN),
            FadeOut(market_group),
            FadeOut(sports_group),
            run_time=AnimationConfig.ZOOM_DURATION
        )
        
        self.play(
            FadeOut(kitchen_group),
            run_time=AnimationConfig.TRANSITION_DURATION
        )
        
        # Mostrar escena de cocina
        kitchen_scene = self.show_kitchen_scene()
        
        # Transición a vista general después de cocina
        self.play(
            FadeOut(kitchen_scene),
            FadeIn(market_group),
            FadeIn(sports_group),
            FadeIn(kitchen_group.scale(0.5).move_to(original_kitchen_position)),
            run_time=AnimationConfig.TRANSITION_DURATION
        )
        
        # Escena Deportes
        self.play(
            sports_group.animate.scale(2).move_to(ORIGIN),
            FadeOut(kitchen_group),
            FadeOut(market_group),
            run_time=AnimationConfig.ZOOM_DURATION
        )
        
        self.play(
            FadeOut(sports_group),
            run_time=AnimationConfig.TRANSITION_DURATION
        )
        
        # Mostrar escena de deportes
        sports_scene = self.show_sports_scene()
        
        self.wait(2)

if __name__ == '__main__':
    scene = TasasCotidianas()
    scene.render()