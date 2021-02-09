import rolldecayestimators.special_symbol as ss
import sympy as sp
import sympy.physics.mechanics as me

import rolldecayestimators.special_symbol as ss
import sympy as sp
import sympy.physics.mechanics as me

## Ship:
I = ss.Symbol(name='I',description='total roll inertia',unit='kg*m**2')
B = ss.Symbol(name='B',description='total roll damping',unit='kg*m*/s')
rho = ss.Symbol(name='rho',description='water density',unit='kg/m**3')
g = ss.Symbol(name='g',description='acceleration of gravity',unit='m/s**2')
Disp = ss.Symbol(name='Disp',description='displacement',unit='m**3')
m = ss.Symbol(name='m',description='mass of ship',unit='kg')
GM = ss.Symbol(name='GM', description='metacentric height', unit='m')
omega = ss.Symbol(name='omega', description='Angular velocity of external moment', unit='rad/s')
L_pp = ss.Symbol(name='L_pp',description='ship perpendicular length',unit='m')
beam = ss.Symbol(name='beam',description='ship beam',unit='m')
C_b = ss.Symbol(name='C_b',description='Block coefficient',unit='-')

BK_L = ss.Symbol(name='BK_L',description='Bilge keel length',unit='m')
BK_B = ss.Symbol(name='BK_B',description='Bilge keel height',unit='m')
A_0 = ss.Symbol(name='A_0',description='Mid ship area coefficient',unit='-')
I_xx = ss.Symbol(name='I_xx',description='Roll intertia',unit='kg*m**2')
K_xx = ss.Symbol(name='K_xx',description='Nondimensional roll radius of gyration',unit='-')
kg = ss.Symbol(name='kg',description='Keel to g',unit='m')
T_F = ss.Symbol(name='T_F',description='Draught forward',unit='m')
T_A = ss.Symbol(name='T_A',description='Draught aft',unit='m')
T = ss.Symbol(name='T',description='Mean draught',unit='m')
V = ss.Symbol(name='V',description='Ship speed',unit='m/s')
OG = ss.Symbol(name='OG',description='Distance into water from still water to centre of gravity',unit='m')

## Time:
t = ss.Symbol(name='t',description='time',unit='s')
phi = me.dynamicsymbols('phi')  # Roll angle
#phi = ss.Symbol(name='phi', description='Roll angle', unit='rad')  # Roll angle
phi_dot = phi.diff()
phi_dot_dot = phi_dot.diff()
phi_a = ss.Symbol(name='phi_a', description='Initial roll amplitude', unit='rad')
omega0 = ss.Symbol(name='omega0',description='Natural angular velocity',unit='rad/s')  # Natural roll frequency

## Damping
B_e = ss.Symbol(name='B_e', description='Equivalen linearized damping', unit='Nm/(rad/s)')
omega_hat = ss.Symbol(name='omega_hat', description='Nondimensional roll frequency', unit='-')

B_44_ = ss.Symbol(name='B_44', description='Total roll damping at a certain roll amplitude', unit='Nm/(rad/s)')
B_F = ss.Symbol(name='B_F', description='Friction roll damping', unit='Nm/(rad/s)')
B_W = ss.Symbol(name='B_W', description='Wave roll damping', unit='Nm/(rad/s)')
B_E = ss.Symbol(name='B_E', description='Eddy roll damping', unit='Nm/(rad/s)')
B_E0_hat = ss.Symbol(name='B_E0_HAT', description='Eddy roll damping at zero speed', unit='-')
B_BK = ss.Symbol(name='B_{BK}', description='Bilge keel roll damping', unit='Nm/(rad/s)')
B_L = ss.Symbol(name='B_L', description='Hull lift roll damping', unit='Nm/(rad/s)')

B_44_HAT =  ss.Symbol(name='B_44_HAT', description='Total roll damping at a certain roll amplitude', unit='-')
B_F_HAT = B_F_hat = ss.Symbol(name='B_F_HAT', description='Friction roll damping', unit='-')
B_W_HAT = B_W_hat = ss.Symbol(name='B_W_HAT', description='Wave roll damping', unit='-')
B_E_HAT = B_E_hat = ss.Symbol(name='B_E_HAT', description='Eddy roll damping', unit='-')
B_BK_HAT = B_BK_hat = ss.Symbol(name='B_BK_HAT', description='Bilge keel roll damping', unit='-')
B_L_HAT = B_L_hat = ss.Symbol(name='B_L_HAT', description='Hull lift roll damping', unit='-')

B_1 = ss.Symbol(name='B_1',description='Linear damping coefficient',unit='Nm/(rad/s)')  # Natural roll frequency
B_2 = ss.Symbol(name='B_2',description='Quadratic damping coefficient',unit='Nm/(rad/s**2')  # Natural roll frequency
B_3 = ss.Symbol(name='B_3',description='Cubic damping coefficient',unit='Nm/(rad/s)**3')  # Natural roll frequency

C = ss.Symbol(name='C', description='General stiffness coefficient', unit=r'Nm/rad')  # Introducing a helper coefficient C

C_1 = ss.Symbol(name='C_1', description='Linear stiffness coefficient', unit=r'Nm/rad')
C_3 = ss.Symbol(name='C_3',description='Stiffness coefficient', unit=r'Nm/rad**3')
C_5 = ss.Symbol(name='C_5',description='Stiffness coefficient', unit=r'Nm/rad**5')

## Analytical
zeta = sp.symbols('zeta')
y = me.dynamicsymbols('y')
y0 = me.dynamicsymbols('y0')
y0_dot = y0.diff()
y0_dotdot = y0_dot.diff()
D = sp.symbols('D')

phi_0 = me.dynamicsymbols('phi_0')
phi_0_dot = phi_0.diff()
phi_0_dotdot = phi_0_dot.diff()

"""
Ikeda, Y.,
1978. On eddy making component of roll damping force on naked hull. University of Osaka Prefacture,
Department of Naval Architecture, Japan, Report No. 00403,
Published in: Journal of Society of Naval Architects of Japan, Volume 142.
"""
C_P =  ss.Symbol(name='C_P', description='Pressure difference coefficient', unit='-')
C_r =  ss.Symbol(name='C_r', description='Eddy damping coefficient', unit='-')
r_max = ss.Symbol(name='r_max', description='Maximum distance from roll axis to hull', unit='m')
P_m = ss.Symbol(name='P_m', description='Pressure difference', unit='N/m**2')
R_b = ss.Symbol(name='R_b', description='Bilge radius', unit='m')
f_1 = ss.Symbol(name='f_1', description='Difference of flow factor', unit='-')
f_2 = ss.Symbol(name='f_2', description='Modification factor', unit='-')
H_0 = ss.Symbol(name='H_0', description='Half beam-draft ratio', unit='-')
B_E_star_hat = ss.Symbol(name='B_E_star_hat', description='Only nonlinear nondimensional damping', unit='-')

## Lewis
a_1 = ss.Symbol(name='a_1', description='Lewis section coefficient', unit='-')
a_3 = ss.Symbol(name='a_3', description='Lewis section coefficient', unit='-')
D_1= ss.Symbol(name='D_1', description='Lewis section coefficient', unit='-')