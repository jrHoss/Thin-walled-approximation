from Base import Base
from CombinedSection import Combined_section

Base.setLogfileName("twp_output.txt")
Base.appendLog("First text for the logfile!")

# all section values are in mm.
# T_section Properties dimensions.
##          ! height
##          !    ! width
##          !    !     ! Thickness
T_section = [140, 140, 15]
# I_section dimensions.
##           ! height.
##           !   ! width.
##           !   !   ! web-Thickness.
##           !   !   !    ! web-Thickness.
I_section = [80, 42, 3.9, 5.9]
# Pipe section dimensions.
##     ! Diameter.
##     !     ! Thickness
Pipe = [48.3, 2.3]

beam_length = 4.4                           # m
load = 39                                   # KN
E = 210                                     # E
CheckCombinedSection = True

if CheckCombinedSection:
    p = Combined_section(T_section[0], T_section[1], T_section[2],
                         I_section[0], I_section[1], I_section[2], I_section[3],
                         Pipe[0], Pipe[1],
                         beam_length, load, E)
    p.logData()
    p.Calculate_deflection()
    p.view()

