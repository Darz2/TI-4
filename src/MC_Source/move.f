      Subroutine Move(Av1,Av2,Delta)
      Implicit None

      Include 'commons.inc'

C     Displace A Randomly Selected Particle

      Logical Laccept
      Integer Ipart,Selectint
      Double Precision Rxn,Ryn,Rzn,Xi,Yi,Zi,Ran_Uniform,Unew,Uold
     $     ,Dunew,Duold,Virold,Virnew,Av1,Av2,Delta

      Ipart = Selectint(Npart)
   
      Rxn = Rx(Ipart) + (2.0d0*Ran_Uniform()-1.0d0)*Delta
      Ryn = Ry(Ipart) + (2.0d0*Ran_Uniform()-1.0d0)*Delta
      Rzn = Rz(Ipart) + (2.0d0*Ran_Uniform()-1.0d0)*Delta

C     Put Back In The Box

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

      Av2 = Av2 + 1.0d0

C     Accept Or Reject

      If(Laccept) Then
         Av1 = Av1 + 1.0d0

         Etotal  = Etotal  + Unew   - Uold
         Dudltot = Dudltot + Dunew  - Duold
         Virial  = Virial  + Virnew - Virold

         Rx(Ipart) = Rxn
         Ry(Ipart) = Ryn
         Rz(Ipart) = Rzn
      Endif

      Return
      End
