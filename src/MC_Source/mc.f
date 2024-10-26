      Program Mc
      Implicit None

C     Monte Carlo In Nvt Ensemble

      Include 'commons.inc'

      Logical Linit
      Integer Ncycle,Ninit,Nmove,I,J,Icycle,Icycle2
      Double Precision Temp,Deltax,V,E,W,Avd1,Avd2,Av1,Av2,Av3,Av4,Avt1
     $     ,Avt2,Avt3,Avt4

      Avd1 = 0.0d0
      Avd2 = 0.0d0

      Av1 = 0.0d0
      Av2 = 0.0d0
      Av3 = 0.0d0
      Av4 = 0.0d0

      Avt1 = 0.0d0
      Avt2 = 0.0d0
      Avt3 = 0.0d0
      Avt4 = 0.0d0

      Open(21,File="Input",Status="Unknown")
      Read(21,*)
      Read(21,*) Ncycle,Ninit,Npart,Linit,Temp,Lambda
      Read(21,*)
      Read(21,*) Deltax,Box
      Read(21,*)
      Read(21,*) Alpha,Rcut
      Close(21)
      
      Beta = 1.0d0/Temp
      Rcutsq = Rcut*Rcut

      If(Lambda.Gt.1.0d0) Lambda = 1.0d0
      If(Lambda.Lt.0.0d0) Lambda = 0.0d0

      Write(6,*) 'Ncycle               : ',Ncycle
      Write(6,*) 'Ninit                : ',Ninit
      Write(6,*) 'Linit                : ',Linit
      Write(6,*) 'Temp                 : ',Temp
      Write(6,*) 'Beta                 : ',Beta
      Write(6,*) 'Lambda               : ',Lambda
      Write(6,*) 'Rcut                 : ',Rcut
      Write(6,*) 'Alpha                : ',Alpha
      Write(6,*) 'Deltax               : ',Deltax
          
      If(Temp.Le.0.0d0)          Stop "Error Temperature !!!"
      If(Deltax.Lt.0.0d0)        Stop "Error Deltax !!"
      If(Ncycle.Lt.100)          Stop "Minimal 100 Cycles !!!"
      If(Alpha.Lt.0.0d0)         Stop "Error Alpha less than 0 !!!"
      If(Alpha.Gt.1.0d0)         Stop "Error Alpha greater than 1 !!!"
      If(Box.Lt.2.0d0*Rcut)      Stop "Box Too Small !!"
      If(Deltax.Gt.0.5d0*Box)    Stop "Error Deltax Too Large !!!"
      
      If(Rcut.Lt.2.0d0) Then
         Write(6,*) 'Rcut is less than 2'
         If(Rcut.Eq.1.2d0) Then   
            Write(6,*) 'Rcut is equal to 1.2 (Colloids)'
         Else
            Stop "Error Rcut is not equal to 1.2 !!!"
         Endif
      Endif   

      If(Linit) Then
         Write(6,*)
         Write(6,*) 'Generate Initial Coordinates'
         Write(6,*)

         If(Npart.Lt.0.Or.Npart.Gt.Maxpart) Stop "Error Npart !!!"
       
         Call Init
      Else
         Write(6,*)
         Write(6,*) 'Read Coordinates From Disk'
         Write(6,*)

         Open(21,File="Coordold",Status="Unknown")
         Read(21,*) Box
         Read(21,*) Npart

         If(Npart.Lt.0.Or.Npart.Gt.Maxpart) Stop "Error Npart !!!"
         If(Box.Lt.2.0d0*Rcut) Stop "Box Too Small !!"
         
         Do I=1,Npart
            Read(21,*) Rx(I),Ry(I),Rz(I)
         Enddo
      Endif
      
      Write(6,*) 'Box                  : ',Box
      Write(6,*) 'Npart                : ',Npart
      Write(6,*) 'Rho                  : ',Dble(Npart)/(Box**3)
     
      If(Deltax.Gt.0.5d0*Box) Stop "Deltax Too Large !!!"

      Etotal  = 0.0d0
      Dudltot = 0.0d0
      Virial  = 0.0d0
      
      Call Etot(W,V,E)

      Virial  = W
      Dudltot = V
      Etotal  = E
      
      Write(6,*)
      Write(6,*) 'Initial Energy Box   : ',Etotal
      Write(6,*) 'Initial dUdL         : ',Dudltot
      Write(6,*) 'Initial Virial       : ',Virial
      Write(6,*)

C     Start Of The Simulation

      Write(6,*)
      Write(6,*)
      Write(6,*) 'The Simulation Is Running.....'
      Write(6,*)
      Write(6,*)

      Call Sample_Radial(1)
      
      Open(22,File="Traject.xyz",Status="Unknown")
      Open(23,File="Results",Status="Unknown")
      write(23, '(A)') "         Icycle                Etotal            Dudltot              Virial"

      Do Icycle=1,Ncycle

         Nmove = Max(20,Npart)

         Avt1 = 0.0d0
         Avt2 = 0.0d0
         Avt3 = 0.0d0
         Avt4 = 0.0d0
         
         Do Icycle2=1,Nmove
            Call Move(Avd1,Avd2,Deltax)

            Avt1 = Avt1 + Etotal
            Avt2 = Avt2 + Dudltot
            Avt3 = Avt3 + Virial
            Avt4 = Avt4 + 1.0d0
         Enddo
                
         Write(23,'(4e20.10)') 
     &        Dble(Icycle),
     &        Etotal,Dudltot,Virial

         If(Icycle.Gt.Ninit) Then
            Call Sample_Radial(2)

            Av1 = Av1 + Avt1/Avt4
            Av2 = Av2 + Avt2/Avt4
            Av3 = Av3 + Avt3/Avt4
            Av4 = Av4 + 1.0d0
         Endif

         If(Mod(Icycle,Ncycle/100).Eq.0) Then
            Write(22,*) Npart
            Write(22,*)

            Do J=1,Npart
               Write(22,'(A,3f15.5)') 'Ar  ',
     &              4.0d0*Rx(J),4.0d0*Ry(J),4.0d0*Rz(J)
            Enddo
         Endif
      Enddo

      Close(22)
      Close(23)

      Call Sample_Radial(3)
           
      Write(6,*) 'Frac. Acc. Displ.    : ',Avd1/Max(0.5d0,Avd2)
     
      Open(21,File="Coordnew",Status="Unknown")
      Write(21,*) Box
      Write(21,*) Npart

      Do I=1,Npart
         Write(21,'(3e20.10)') Rx(I),Ry(I),Rz(I)
      Enddo
      Close(21)

C     Check Energy Calculation

      Call Etot(W,V,E)

      Write(6,*)
      Write(6,*) 'Average Energy       : ',Av1/Av4
      Write(6,*) 'Average dUdL         : ',Av2/Av4
      Write(6,*) 'Average Virial       : ',Av3/Av4
      Write(6,*)
      Write(6,*) 'Energy               : ',E
      Write(6,*) 'Energy Sim.          : ',Etotal
      Write(6,*) 'Diff                 : ',Dabs(Etotal-E)
      Write(6,*) 'dUdL                 : ',V
      Write(6,*) 'dUdL Sim.            : ',Dudltot
      Write(6,*) 'Diff                 : ',Dabs(Dudltot-V)
      Write(6,*) 'Virial               : ',W
      Write(6,*) 'Virial Sim.          : ',Virial
      Write(6,*) 'Diff                 : ',Dabs(Virial-W)
      Write(6,*)
      
      Stop
      End
