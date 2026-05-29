from object_library import all_form_factors, FormFactor
import parameters as Param

GIP_Damping = FormFactor(name = 'GIP_Damping',
                         type = 'real',
                         value = 'cmath.exp(-P(0,3)**2 / Param.OmegaGIP**2)')
