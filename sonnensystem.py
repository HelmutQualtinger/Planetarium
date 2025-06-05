from vpython import *
import random

# Fensterkonfiguration
scene.title = "Sonnensystem"
scene.width = 1200
scene.height = 800
scene.background = color.black
scene.range = 2.5  # Zoomfaktor

# Zeitskalierung - ERHÖHT für sichtbare Bewegung
dt = 0.01  # Zeitschritt erhöht (war 0.001)
rate_value = 100  # Bilder pro Sekunde reduziert für stabilere Leistung

# Hilfsfunktion für elliptische Bahnen mit Neigung
def elliptical_orbit(a, e, angle=0, inclination=0, node_angle=0):
    """Erstellt Punkte für eine elliptische Bahn
    a: große Halbachse
    e: Exzentrizität (0 = Kreis, 0<e<1 = Ellipse)
    angle: Rotationswinkel der Ellipse in Radiant
    inclination: Neigung der Bahnebene in Radiant
    node_angle: Winkel des aufsteigenden Knotens in Radiant
    """
    points = []
    for theta in range(0, 361, 5):  # Punkte alle 5 Grad
        theta_rad = radians(theta)
        r = a * (1 - e**2) / (1 + e * cos(theta_rad))
        x = r * cos(theta_rad)
        y = r * sin(theta_rad)
        
        # Rotation der Ellipse in der xy-Ebene
        x_rot = x * cos(angle) - y * sin(angle)
        y_rot = x * sin(angle) + y * cos(angle)
        
        # Anwendung des Knotenwinkels (Rotation um die z-Achse)
        x_node = x_rot * cos(node_angle) - y_rot * sin(node_angle)
        y_node = x_rot * sin(node_angle) + y_rot * cos(node_angle)
        
        # Neigung der Bahnebene (Rotation um die neue x-Achse)
        y_incl = y_node * cos(inclination)
        z_incl = y_node * sin(inclination)
        
        points.append(vector(x_node, z_incl, y_incl))
    return points

# Hilfsfunktion zur Berechnung der Position auf einer Ellipse mit Neigung
def position_on_ellipse(a, e, angle, inclination, node_angle, theta):
    """
    a: große Halbachse
    e: Exzentrizität
    angle: Rotation der Ellipse
    inclination: Neigung der Bahnebene in Radiant
    node_angle: Winkel des aufsteigenden Knotens in Radiant
    theta: Position auf der Ellipse (0-2pi)
    """
    r = a * (1 - e**2) / (1 + e * cos(theta))
    x = r * cos(theta)
    y = r * sin(theta)
    
    # Rotation der Ellipse in der xy-Ebene
    x_rot = x * cos(angle) - y * sin(angle)
    y_rot = x * sin(angle) + y * cos(angle)
    
    # Anwendung des Knotenwinkels (Rotation um die z-Achse)
    x_node = x_rot * cos(node_angle) - y_rot * sin(node_angle)
    y_node = x_rot * sin(node_angle) + y_rot * cos(node_angle)
    
    # Neigung der Bahnebene (Rotation um die neue x-Achse)
    y_incl = y_node * cos(inclination)
    z_incl = y_node * sin(inclination)
    
    return vector(x_node, z_incl, y_incl)

# Hilfsfunktion für die Erstellung eines Rings
def create_ring(planet_pos, axis, radius):
    """Erstellt ein einzelnes Ringobjekt."""
    return ring(pos=planet_pos, axis=axis, radius=radius, thickness=0.002, color=vector(0.9, 0.8, 0.6), opacity=0.7)

# Hilfsfunktion für die Erstellung von Ringen
def create_rings(planet_pos, inner_radius, outer_radius, num_rings, inclination, node_angle=0):
    rings_list = []  # Umbenannt von "rings" zu "rings_list"
    ring_spacing = (outer_radius - inner_radius) / num_rings
    
    # Berechnung der Achse für die Ringe unter Berücksichtigung von Neigung und Knotenwinkel
    axis = vector(0, 1, 0)
    # Rotation um die x-Achse (Neigung)
    y_rot = axis.y * cos(inclination)
    z_rot = axis.y * sin(inclination)
    axis_incl = vector(axis.x, y_rot, z_rot)
    # Rotation um die z-Achse (Knotenwinkel)
    x_node = axis_incl.x * cos(node_angle) - axis_incl.y * sin(node_angle)
    y_node = axis_incl.x * sin(node_angle) + axis_incl.y * cos(node_angle)
    final_axis = vector(x_node, axis_incl.z, y_node)
    
    for i in range(num_rings):
        r = inner_radius + i * ring_spacing
        # Verwende "ring_obj" statt "ring" für die Variable
        ring_obj = create_ring(planet_pos, final_axis, r)
        rings_list.append(ring_obj)
    
    return rings_list

# Kepler's drittes Gesetz: T² ∝ a³
# Berechnung der Umlaufgeschwindigkeit basierend auf der großen Halbachse
def orbital_velocity(a):
    """
    Berechnet die Umlaufgeschwindigkeit eines Körpers basierend auf seiner Entfernung zur Sonne
    gemäß Kepler's drittem Gesetz
    a: große Halbachse
    """
    # Wir verwenden die Erde als Referenz (a=1, T=1 Jahr)
    # v ∝ 1/√a, da v = 2πa/T und T² ∝ a³, also T ∝ a^(3/2) und v ∝ a/a^(3/2) = 1/a^(1/2)
    return 2.0 / sqrt(a)  # ERHÖHT für bessere Sichtbarkeit (war 0.26)

# Hilfsfunktion für die Position eines Mondes
def position_moon(planet_pos, distance, theta, inclination, node_angle):
    # Erst die Position in der Bahnebene berechnen
    moon_local_x = distance * cos(theta)
    moon_local_y = distance * sin(theta)
    
    # Anwendung des Knotenwinkels
    moon_x = moon_local_x * cos(node_angle) - moon_local_y * sin(node_angle)
    moon_y = moon_local_x * sin(node_angle) + moon_local_y * cos(node_angle)
    
    # Anwendung der Neigung
    moon_y_incl = moon_y * cos(inclination)
    moon_z_incl = moon_y * sin(inclination)
    
    return planet_pos + vector(moon_x, moon_z_incl, moon_y_incl)

# Himmelskörper erstellen
# Sonne
sun = sphere(pos=vector(0, 0, 0), radius=0.2, color=color.yellow,
             emissive=True)

# Merkur
mercury_a = 0.4  # Große Halbachse
mercury_e = 0.206  # Exzentrizität
mercury_inc = radians(25.0)  # Stark erhöhte Neigung
mercury_node = radians(30)   # Winkel des aufsteigenden Knotens
mercury_orbit_points = elliptical_orbit(mercury_a, mercury_e, radians(20), mercury_inc, mercury_node)
mercury_orbit = curve(pos=mercury_orbit_points, color=color.gray(0.5))
mercury = sphere(pos=mercury_orbit_points[0], radius=0.03, 
                 color=color.gray(0.7), make_trail=True, 
                 trail_radius=0.001, trail_color=color.gray(0.5), 
                 retain=30)  # retain=30 für kurze Spur
mercury.velocity = orbital_velocity(mercury_a) * 1.2

# Venus
venus_a = 0.7
venus_e = 0.007
venus_inc = radians(40.0)  # Stark erhöhte Neigung
venus_node = radians(90)   # Anderer Knotenwinkel
venus_orbit_points = elliptical_orbit(venus_a, venus_e, radians(10), venus_inc, venus_node)
venus_orbit = curve(pos=venus_orbit_points, color=color.orange)
venus = sphere(pos=venus_orbit_points[0], radius=0.06, 
               color=color.orange, make_trail=True, 
               trail_radius=0.001, trail_color=color.orange, 
               retain=30)  # retain=30 für kurze Spur
venus.velocity = orbital_velocity(venus_a) * 1.0

# Erde
earth_a = 1.0
earth_e = 0.017
earth_inc = radians(0.0)  # Referenzebene (keine Neigung)
earth_node = radians(0)   # Kein Knotenwinkel (Referenzebene)
earth_orbit_points = elliptical_orbit(earth_a, earth_e, 0, earth_inc, earth_node)
earth_orbit = curve(pos=earth_orbit_points, color=color.blue)
earth = sphere(pos=earth_orbit_points[0], radius=0.06, 
               color=color.blue, make_trail=True, 
               trail_radius=0.001, trail_color=color.blue, 
               retain=30)  # retain=30 für kurze Spur
earth.velocity = orbital_velocity(earth_a) * 1.0

# Mond
moon_radius = 0.02
moon_distance = 0.12  # Entfernung von der Erde
moon_inc = radians(30.0)  # Stark erhöhte Neigung zur Erdbahn
moon_node = radians(60)   # Knotenwinkel des Mondes
moon = sphere(pos=earth.pos + vector(moon_distance, 0, 0), 
              radius=moon_radius, color=color.gray(0.8), 
              make_trail=True, trail_radius=0.001, 
              trail_color=color.gray(0.5), retain=30)  # retain=30 für kurze Spur
moon.velocity = earth.velocity  # Gleiche Basisgeschwindigkeit wie die Erde
moon.orbit_speed = 2.0  # Relative Geschwindigkeit um die Erde

# Mars
mars_a = 1.5
mars_e = 0.093
mars_inc = radians(35.0)  # Stark erhöhte Neigung
mars_node = radians(150)  # Anderer Knotenwinkel
mars_orbit_points = elliptical_orbit(mars_a, mars_e, radians(15), mars_inc, mars_node)
mars_orbit = curve(pos=mars_orbit_points, color=color.red)
mars = sphere(pos=mars_orbit_points[0], radius=0.05, 
              color=color.red, make_trail=True, 
              trail_radius=0.001, trail_color=color.red, 
              retain=30)  # retain=30 für kurze Spur
mars.velocity = orbital_velocity(mars_a) * 0.8

# Jupiter
jupiter_a = 2.1
jupiter_e = 0.048
jupiter_inc = radians(20.0)  # Erhöhte Neigung
jupiter_node = radians(210)  # Anderer Knotenwinkel
jupiter_orbit_points = elliptical_orbit(jupiter_a, jupiter_e, radians(5), jupiter_inc, jupiter_node)
jupiter_orbit = curve(pos=jupiter_orbit_points, color=color.orange)
jupiter = sphere(pos=jupiter_orbit_points[0], radius=0.12, 
                 color=vector(0.8, 0.7, 0.5), make_trail=True, 
                 trail_radius=0.005, trail_color=color.orange)
jupiter.velocity = orbital_velocity(jupiter_a) * 0.5

# Galileische Monde des Jupiter
# Io
io_distance = 0.18
io_radius = 0.02
io_inc = radians(10.0)
io_node = radians(20)
io = sphere(pos=jupiter.pos + vector(io_distance, 0, 0), 
            radius=io_radius, color=color.yellow, 
            make_trail=True, trail_radius=0.001, 
            trail_color=color.yellow)
io.orbit_speed = 3.0

# Europa
europa_distance = 0.22
europa_radius = 0.018
europa_inc = radians(15.0)
europa_node = radians(60)
europa = sphere(pos=jupiter.pos + vector(europa_distance, 0, 0), 
                radius=europa_radius, color=color.white, 
                make_trail=True, trail_radius=0.001, 
                trail_color=color.white)
europa.orbit_speed = 2.2

# Ganymed
ganymede_distance = 0.28
ganymede_radius = 0.025
ganymede_inc = radians(20.0)
ganymede_node = radians(100)
ganymede = sphere(pos=jupiter.pos + vector(ganymede_distance, 0, 0), 
                  radius=ganymede_radius, color=vector(0.6, 0.6, 0.6), 
                  make_trail=True, trail_radius=0.001, 
                  trail_color=vector(0.6, 0.6, 0.6))
ganymede.orbit_speed = 1.7

# Kallisto
callisto_distance = 0.35
callisto_radius = 0.022
callisto_inc = radians(25.0)
callisto_node = radians(140)
callisto = sphere(pos=jupiter.pos + vector(callisto_distance, 0, 0), 
                  radius=callisto_radius, color=vector(0.4, 0.4, 0.4), 
                  make_trail=True, trail_radius=0.001, 
                  trail_color=vector(0.4, 0.4, 0.4))
callisto.orbit_speed = 1.2

# Saturn
saturn_a = 2.7
saturn_e = 0.056
saturn_inc = radians(15.0)
saturn_node = radians(270)
saturn_orbit_points = elliptical_orbit(saturn_a, saturn_e, radians(8), saturn_inc, saturn_node)
saturn_orbit = curve(pos=saturn_orbit_points, color=color.orange)
saturn = sphere(pos=saturn_orbit_points[0], radius=0.11, 
                color=vector(0.9, 0.8, 0.6), make_trail=True, 
                trail_radius=0.005, trail_color=color.orange)
saturn.velocity = orbital_velocity(saturn_a) * 0.4

# Saturnringe
saturn_rings = []
saturn_ring_inner = 0.13
saturn_ring_outer = 0.25
saturn_ring_count = 5
saturn_ring_inc = radians(27)  # Neigung der Ringe

# Anfangsringe erstellen
saturn_rings = create_rings(saturn.pos, saturn_ring_inner, saturn_ring_outer, 
                           saturn_ring_count, saturn_ring_inc, saturn_node)

# Steuerung
time_factor = 3.0  # ERHÖHT für schnellere Bewegung
running = True

def keydown(evt):
    global time_factor, running
    if evt.key == '+':
        time_factor *= 1.5
    elif evt.key == '-':
        time_factor /= 1.5
    elif evt.key == ' ':
        running = not running

scene.bind('keydown', keydown)

instructions = label(pos=vector(0, 1.7, 0), 
                     text="+ oder - : Zeitfaktor ändern\nLeertaste: Pause/Fortsetzen",
                     height=15, color=color.white, box=False)

# Zufällige Anfangspositionen für die Planeten und Monde
mercury_theta = random.random() * 2 * pi
venus_theta = random.random() * 2 * pi
earth_theta = random.random() * 2 * pi
mars_theta = random.random() * 2 * pi
jupiter_theta = random.random() * 2 * pi
saturn_theta = random.random() * 2 * pi
moon_theta = random.random() * 2 * pi
io_theta = random.random() * 2 * pi
europa_theta = random.random() * 2 * pi
ganymede_theta = random.random() * 2 * pi
callisto_theta = random.random() * 2 * pi

# Anfangspositionen setzen
mercury.pos = position_on_ellipse(mercury_a, mercury_e, radians(20), mercury_inc, mercury_node, mercury_theta)
venus.pos = position_on_ellipse(venus_a, venus_e, radians(10), venus_inc, venus_node, venus_theta)
earth.pos = position_on_ellipse(earth_a, earth_e, 0, earth_inc, earth_node, earth_theta)
mars.pos = position_on_ellipse(mars_a, mars_e, radians(15), mars_inc, mars_node, mars_theta)
jupiter.pos = position_on_ellipse(jupiter_a, jupiter_e, radians(5), jupiter_inc, jupiter_node, jupiter_theta)
saturn.pos = position_on_ellipse(saturn_a, saturn_e, radians(8), saturn_inc, saturn_node, saturn_theta)

# Monde-Positionen aktualisieren
moon.pos = position_moon(earth.pos, moon_distance, moon_theta, moon_inc, moon_node)
io.pos = position_moon(jupiter.pos, io_distance, io_theta, io_inc, io_node)
europa.pos = position_moon(jupiter.pos, europa_distance, europa_theta, europa_inc, europa_node)
ganymede.pos = position_moon(jupiter.pos, ganymede_distance, ganymede_theta, ganymede_inc, ganymede_node)
callisto.pos = position_moon(jupiter.pos, callisto_distance, callisto_theta, callisto_inc, callisto_node)

# Saturnringe aktualisieren
for saturn_ring in saturn_rings:
    saturn_ring.visible = False
saturn_rings = create_rings(saturn.pos, saturn_ring_inner, saturn_ring_outer, 
                           saturn_ring_count, saturn_ring_inc, saturn_node)

# Kamerasteuerung hinzufügen
scene.caption = "Verwende die Maus zum Rotieren, Scrollen zum Zoomen"

# Debug-Anzeige für die Geschwindigkeiten
velocity_label = label(pos=vector(0, -1.7, 0), 
                       text=f"Merkur: {mercury.velocity:.2f}, Erde: {earth.velocity:.2f}, Jupiter: {jupiter.velocity:.2f}",
                       height=10, color=color.white, box=False)

print("Geschwindigkeiten:", mercury.velocity, venus.velocity, earth.velocity, mars.velocity, jupiter.velocity, saturn.velocity)

# Hauptschleife
while True:
    rate(rate_value)
    if not running:
        continue
        
    # Zeit-Update
    time_step = dt * time_factor
    
    # Merkur-Update
    mercury_theta += mercury.velocity * time_step
    if mercury_theta > 2*pi:
        mercury_theta -= 2*pi
    mercury.pos = position_on_ellipse(mercury_a, mercury_e, radians(20), mercury_inc, mercury_node, mercury_theta)
    
    # Venus-Update
    venus_theta += venus.velocity * time_step
    if venus_theta > 2*pi:
        venus_theta -= 2*pi
    venus.pos = position_on_ellipse(venus_a, venus_e, radians(10), venus_inc, venus_node, venus_theta)
    
    # Erde-Update
    earth_theta += earth.velocity * time_step
    if earth_theta > 2*pi:
        earth_theta -= 2*pi
    earth.pos = position_on_ellipse(earth_a, earth_e, 0, earth_inc, earth_node, earth_theta)
    
    # Mond-Update
    moon_theta += moon.orbit_speed * time_step
    if moon_theta > 2*pi:
        moon_theta -= 2*pi
    moon.pos = position_moon(earth.pos, moon_distance, moon_theta, moon_inc, moon_node)
    
    # Mars-Update
    mars_theta += mars.velocity * time_step
    if mars_theta > 2*pi:
        mars_theta -= 2*pi
    mars.pos = position_on_ellipse(mars_a, mars_e, radians(15), mars_inc, mars_node, mars_theta)
    
    # Jupiter-Update
    jupiter_theta += jupiter.velocity * time_step
    if jupiter_theta > 2*pi:
        jupiter_theta -= 2*pi
    jupiter.pos = position_on_ellipse(jupiter_a, jupiter_e, radians(5), jupiter_inc, jupiter_node, jupiter_theta)
    
    # Galileische Monde-Update
    # Io
    io_theta += io.orbit_speed * time_step
    if io_theta > 2*pi:
        io_theta -= 2*pi
    io.pos = position_moon(jupiter.pos, io_distance, io_theta, io_inc, io_node)
    
    # Europa
    europa_theta += europa.orbit_speed * time_step
    if europa_theta > 2*pi:
        europa_theta -= 2*pi
    europa.pos = position_moon(jupiter.pos, europa_distance, europa_theta, europa_inc, europa_node)
    
    # Ganymed
    ganymede_theta += ganymede.orbit_speed * time_step
    if ganymede_theta > 2*pi:
        ganymede_theta -= 2*pi
    ganymede.pos = position_moon(jupiter.pos, ganymede_distance, ganymede_theta, ganymede_inc, ganymede_node)
    
    # Kallisto
    callisto_theta += callisto.orbit_speed * time_step
    if callisto_theta > 2*pi:
        callisto_theta -= 2*pi
    callisto.pos = position_moon(jupiter.pos, callisto_distance, callisto_theta, callisto_inc, callisto_node)
    
    # Saturn-Update
    saturn_theta += saturn.velocity * time_step
    if saturn_theta > 2*pi:
        saturn_theta -= 2*pi
    saturn.pos = position_on_ellipse(saturn_a, saturn_e, radians(8), saturn_inc, saturn_node, saturn_theta)
    
    # Saturnringe aktualisieren
    for sring in saturn_rings:
        sring.visible = False  # Alten Ring entfernen
    
    # Neue Ringe erstellen an der aktuellen Saturn-Position
    saturn_rings = create_rings(saturn.pos, saturn_ring_inner, saturn_ring_outer, 
                               saturn_ring_count, saturn_ring_inc, saturn_node)