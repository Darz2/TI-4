      Subroutine Epart(Vir,Dudl,Upot,Xi,Yi,Zi,Ipart)
      Implicit None

      Include 'commons.inc'

C     Compute The Energy Of Particle Ipart

      Integer I,Ipart
      Double Precision Vir,Dudl,Upot,Dx,Dy,Dz,R2,Bx,Hbx,Xi,Yi,Zi,F0,F1,F2,F3
     $     ,F4,F5,C0,C1,C2

      Upot = 0.0d0
      Dudl = 0.0d0
      Vir  = 0.0d0

      Bx  = Box
      Hbx = 0.5d0*Box

      C0 = Alpha*(1.0d0-Lambda)
      C1 = Alpha*(1.0d0-Lambda) + Rcutsq
      C2 = Alpha*Lambda

      Do I=1,Npart

         If(I.Ne.Ipart) Then

            Dx = Rx(I)-Xi
            Dy = Ry(I)-Yi
            Dz = Rz(I)-Zi
            
            If (Dx.Gt.Hbx) Then
               Dx = Dx - Bx
            Elseif (Dx.Lt.-Hbx) Then
               Dx = Dx + Bx
            Endif
                  
            If (Dy.Gt.Hbx) Then
               Dy = Dy - Bx
            Elseif (Dy.Lt.-Hbx) Then
               Dy = Dy + Bx
            Endif
                  
            If (Dz.Gt.Hbx) Then
               Dz = Dz - Bx
            Elseif (Dz.Lt.-Hbx) Then
               Dz = Dz + Bx
            Endif

            R2 = Dx**2 + Dy**2 + Dz**2

            If(R2.Lt.Rcutsq) Then
               F0 = C0 + R2
               F1 = 1.0d0/F0
               F2 = C1*F1  - 1.0d0
               F3 = Rcutsq - R2
               F4 = F0     - 1.0d0
               F5 = F1*F1*F1*F1
               
               Upot = Upot + Lambda*(F1 - 1.0d0)*F2*F2
               
               Dudl = Dudl + F3*(-F3*F0*F4 - 2.0d0*F3*C2*F4 + F3*C2)
     &              *F5

               Vir = Vir - 2.0d0*F5*F3*Lambda*R2*(F3 - 2.0d0*F4*C1)
               
            Endif
         Endif
      Enddo

      Return
      End
