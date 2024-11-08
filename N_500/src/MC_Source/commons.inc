C     Global Variables

      Integer Maxpart

      Parameter (Maxpart = 1000)

      Double Precision Alpha,Rcut,Rcutsq

C      Parameter (Alpha  = 0.5d0)
C      Parameter (Rcut   = 2.0d0)
C      Parameter (Rcutsq = Rcut*Rcut)

      Integer Npart

      Double Precision Rx(Maxpart),Ry(Maxpart),Rz(Maxpart),Box
     $     ,Beta,Etotal,Dudltot,Virial,Lambda

      Common /Mycomms/ Rx,Ry,Rz,Box,Beta,Etotal
     $     ,Dudltot,Virial,Lambda,Alpha,Rcut,Rcutsq,Npart
