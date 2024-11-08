      Subroutine Sample_Radial(Ichoise)
      Implicit None

      Include 'commons.inc'

C     Samples The Radial Distribution Function

      Integer Maxbin

      Parameter(Maxbin = 2000)

      Double Precision Delta,Idelta,Int1,Int2,Glng

      Parameter (Delta  = 0.01d0)
      Parameter (Idelta = 1.0d0/Delta)

      Integer I,J,K,Ichoise

      Double Precision Ggt,Gg(Maxbin),R2,Dx,Dy,Dz,Bx,Hbx,Vol,Nexp,Nex
     $     ,Scale(Maxbin)

      Save Ggt,Gg

      Bx  = Box
      Hbx = 0.5d0*Box

      If(Ichoise.Eq.1) Then
         
         Do I=1,Maxbin
            Gg(I) = 0.0d0
         Enddo

         Ggt = 0.0d0
      
      Elseif(Ichoise.Eq.2) Then

         Ggt = Ggt + 1.0d0

C     Loop Over All Pairs

         Do I=1,Npart-1
            Do J=I+1,Npart

               Dx = Rx(I) - Rx(J)
               Dy = Ry(I) - Ry(J)
               Dz = Rz(I) - Rz(J)
 
               If (Dx.Gt.Hbx) Then
                  Dx = Dx - Bx
               Elseif (Dx.Lt. - Hbx) Then
                  Dx = Dx + Bx
               Endif
 
               If (Dy.Gt.Hbx) Then
                  Dy = Dy - Bx
               Elseif (Dy.Lt. - Hbx) Then
                  Dy = Dy + Bx
               Endif
 
               If (Dz.Gt.Hbx) Then
                  Dz = Dz - Bx
               Elseif (Dz.Lt. - Hbx) Then
                  Dz = Dz + Bx
               Endif

               R2 = Dsqrt(Dx*Dx + Dy*Dy + Dz*Dz)

               If(R2.Lt.Hbx) Then

                  K = 1 + Int(R2*Idelta)

                  If(K.Le.Maxbin) Then
                     Gg(K) = Gg(K) + 2.0d0
                  Else
                     Stop "Error Maxbin"
                  Endif
               Endif
            Enddo
         Enddo

      Else

C     Write Results To Disk

         Do I=1,Maxbin

            If((Dble(I)-0.5d0)*Delta.Lt.Hbx) Then
               
               R2 = (16.0d0*Datan(1.0d0)/3.0d0)*
     &              (1.0d0/(Bx**3))*(Delta**3)*
     &              ((Dble(I))**3 - (Dble(I-1)**3))*Ggt*(Dble(Npart)**2)
               
               Gg(I) = Gg(I)/R2
            Endif
         Enddo

C     van der Vegt
         
         Do I=1,Maxbin
            Vol = 16.0d0*Datan(1.0d0)*
     &           (((Dble(I)-0.5d0)*Delta)**3)/3.0d0
               
            Nexp = Dble(Npart)*(1.0d0-Vol/(Box**3))

            Nex = 0.0d0

            Do J=1,I
               Nex = Nex + Dble(Npart)*(Gg(J) - 1.0d0)*16.0d0*Datan(1.0d0)*
     &              (((Dble(J)-0.5d0)*Delta)**2)*Delta/(Box**3)
            Enddo

            Scale(I) = Nexp/(Nexp - Nex - 1.0d0)
         Enddo

C     print RDF to disk

         Open(21,File="Radial",Status="Unknown")
         write(21, '(A)') "      Distance(R2)         g(r)           g(r)*vdvcorrection   vdvcorrection"
         Do I=1,Maxbin

            If((Dble(I)-0.5d0)*Delta.Lt.Hbx)
     &           Write(21,'(4e20.10)')
     &           (Dble(I)-0.5d0)*Delta,Gg(I),Gg(I)*Scale(I),Scale(I)
            
         Enddo
         Close(21)

C     Integrate Gr

         Int1 = 0.0d0
         Int2 = 0.0d0

         Open(21,File="Integral",Status="Unknown")
         write(21, '(A)') "    Distance(R2)          g(r)            g(r)-van_der_vegt"

         Do I=1,Maxbin

            R2 = Dble(I)*Delta
            
            If(R2.Lt.Hbx) Then

               Int1 = Int1 + Delta*
     &              (Glng(Gg(I)) - Gg(I) + 1.0d0)*
     &              ((Dble(I)-0.5d0)*Delta)**2

               Int2 = Int2 + Delta*
     &              (Glng(Gg(I)*Scale(I)) - Gg(I)*Scale(I) + 1.0d0)*
     &              ((Dble(I)-0.5d0)*Delta)**2
               
               Write(21,'(3e20.10)') R2,Int1,Int2
     
            Endif
         Enddo
         
         Close(21)
         
      Endif

      Return
      End
