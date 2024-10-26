      Subroutine Init
      Implicit None

      Include 'commons.inc'

C     Generate An Initial Configuration

      Logical Laccept
      Integer I,J,Ipart,Selectint
      Double Precision Ran_Uniform,Xi,Yi,Zi,Rxn,Ryn,Rzn,Unew,Uold
     $     ,Dunew,Duold,Virold,Virnew

C     Generate Random Coordinates

      Do I=1,Npart
         Rx(I) = Box*Ran_Uniform()
         Ry(I) = Box*Ran_Uniform()
         Rz(I) = Box*Ran_Uniform()
      Enddo

C     Monte Carlo Displacements To Remove Initial Overlaps

      Do J=1,Npart*50
         Ipart = Selectint(Npart)

         Rxn = Rx(Ipart) + Ran_Uniform() - 0.5d0
         Ryn = Ry(Ipart) + Ran_Uniform() - 0.5d0
         Rzn = Rz(Ipart) + Ran_Uniform() - 0.5d0

         If(Rxn.Lt.0.0d0) Then
            Rxn = Rxn + Box
         Elseif(Rxn.Gt.Box) Then
            Rxn = Rxn - Box
         Endif

         If(Ryn.Lt.0.0d0) Then
            Ryn = Ryn + Box
         Elseif(Ryn.Gt.Box) Then
            Ryn = Ryn - Box
         Endif

         If(Rzn.Lt.0.0d0) Then
            Rzn = Rzn + Box
         Elseif(Rzn.Gt.Box) Then
            Rzn = Rzn - Box
         Endif

         Xi = Rx(Ipart)
         Yi = Ry(Ipart)
         Zi = Rz(Ipart)

         Call Epart(Virold,Duold,Uold,Xi,Yi,Zi,Ipart)
         Call Epart(Virnew,Dunew,Unew,Rxn,Ryn,Rzn,Ipart)

         Call Accept(Dexp(-Beta*(Unew-Uold)),Laccept)

         If(Laccept) Then
            Rx(Ipart) = Rxn
            Ry(Ipart) = Ryn
            Rz(Ipart) = Rzn
         Endif
      Enddo

      Return
      End
