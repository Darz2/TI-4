      Function Glng(X)
      Implicit None

      Double Precision Glng,X

      If(X.Lt.1.0d-20) Then
         Glng = 0.0d0
      Else
         Glng = X*Dlog(X)
      Endif

      Return
      End
