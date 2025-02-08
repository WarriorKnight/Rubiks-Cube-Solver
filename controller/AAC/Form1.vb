Imports System.IO.Ports
Imports AForge
Imports AForge.Video
Imports AForge.Video.DirectShow
Imports System.IO
Imports System.Text.RegularExpressions

Public Class Form1

    Dim WithEvents sp As New SerialPort
    Dim baudRate As Integer = 57600
    Dim CAMERA As VideoCaptureDevice
    Dim bmp As Bitmap


    Private Sub GetSerialPortNames()
        ComboBox1.Items.Clear()
        For Each sport As String In My.Computer.Ports.SerialPortNames
            ComboBox1.Items.Add(sport)
        Next
    End Sub

    Sub ShowString(ByVal myString As String)
        'txtIn.AppendText(myString)
    End Sub

    Delegate Sub myMethodDelegate(ByVal [text] As String)
    Dim myDelegate As New myMethodDelegate(AddressOf ShowString)

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Try
            sp.BaudRate = baudRate
            sp.PortName = ComboBox1.SelectedItem.ToString
            sp.Open()
            If sp.IsOpen Then
                Label5.Text = "Status: Connected"
                'Button1.Visible = False
                'ComboBox1.Enabled = False

                'Button2.Visible = True
            End If
        Catch
            Label5.Text = "Status: Connection Failed"
            sp.Close()
        End Try
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Try
            sp.Close()
            'Button1.Visible = True
            'Button2.Visible = False
            'ComboBox1.Enabled = True
            Label5.Text = "Status: Disconnected"
            Exit Sub
        Catch
            Label5.Text = "Status: Failed"
        End Try
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        GetSerialPortNames()
    End Sub

    Public Function SendMove(Move As String)
        If CheckBox1.Checked = True Then
            SendCommand("M " & Move)
        Else
            TextBox1.Text += Move
        End If
    End Function

    Public Function SendCommand(Command As String)
        If sp.IsOpen() Then
            sp.Write(Command)
        End If
    End Function


    Public Function LoadInfo(Info As String)
        Try
            Dim str As String = Info
            Dim numbers As New List(Of Integer)

            For Each word As String In str.Split(" ")
                If IsNumeric(word) Then
                    numbers.Add(CInt(word))
                End If
            Next

            Label8.Text = numbers(0)
            Label9.Text = numbers(1)

        Catch
            MsgBox("Error: Failed to parse info")
        End Try
    End Function

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.MouseDown
        SendMove("F")
    End Sub

    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.MouseDown
        SendMove("f")
    End Sub

    Private Sub Button7_Click(sender As Object, e As EventArgs) Handles Button7.MouseDown
        SendMove("R")
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.MouseDown
        SendMove("r")
    End Sub

    Private Sub Button14_Click(sender As Object, e As EventArgs) Handles Button14.MouseDown
        SendCommand("M " & TextBox1.Text)
    End Sub


    Private Sub Button9_Click(sender As Object, e As EventArgs) Handles Button9.MouseDown
        SendMove("D")
    End Sub

    Private Sub Button8_Click(sender As Object, e As EventArgs) Handles Button8.MouseDown
        SendMove("d")
    End Sub

    Private Sub Button11_Click(sender As Object, e As EventArgs) Handles Button11.MouseDown
        SendMove("L")
    End Sub

    Private Sub Button10_Click(sender As Object, e As EventArgs) Handles Button10.MouseDown
        SendMove("l")
    End Sub

    Private Sub Button13_Click(sender As Object, e As EventArgs) Handles Button13.MouseDown
        SendMove("B")
    End Sub

    Private Sub Button12_Click(sender As Object, e As EventArgs) Handles Button12.MouseDown
        SendMove("b")
    End Sub



    Private Sub Button15_Click(sender As Object, e As EventArgs) Handles Button15.Click
        Try
            sp.BaudRate = baudRate
            sp.PortName = "COM6"
            sp.Open()
            If sp.IsOpen Then
                'Button1.Visible = False
                ComboBox1.Enabled = False
                'Button2.Visible = True
            End If
        Catch
            sp.Close()
        End Try
    End Sub



    'https://learn.microsoft.com/en-us/dotnet/visual-basic/developing-apps/programming/computer-resources/how-to-receive-strings-from-serial-ports

    Function ReceiveSerialData() As String
        Dim returnStr As String = ""

        'Dim com1 As IO.Ports.SerialPort = Nothing
        Try
            'com1 = My.Computer.Ports.OpenSerialPort("COM1")
            sp.ReadTimeout = 10000
            Do
                Dim Incoming As String = sp.ReadLine()
                If Incoming Is Nothing Then
                    Exit Do
                Else
                    returnStr &= Incoming & vbCrLf
                End If
            Loop
        Catch ex As TimeoutException
            returnStr = "Error: Serial Port read timed out."
        Finally
            'If sp IsNot Nothing Then sp.Close()
        End Try

        Return returnStr
    End Function

    Private Sub Button20_Click(sender As Object, e As EventArgs)

    End Sub

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        Try
            If sp.BytesToRead > 0 Then
                Dim receivedData As String = ">> " & sp.ReadLine()
                RichTextBox1.Text += receivedData
                If receivedData.Contains("Info:") Then
                    LoadInfo(receivedData)
                End If
            End If
        Catch
        End Try
    End Sub

    Private Sub Button19_Click(sender As Object, e As EventArgs) Handles Button19.Click
        SendCommand("D " & TextBox2.Text)
        SendCommand("I")
    End Sub

    Private Sub Button18_Click(sender As Object, e As EventArgs) Handles Button18.Click
        SendCommand("S " & TextBox3.Text)
        SendCommand("I")
    End Sub

    Private Sub Button14_Click(sender As Object, e As MouseEventArgs) Handles Button14.MouseDown

    End Sub

    Private Sub Button16_Click(sender As Object, e As EventArgs) Handles Button16.Click
        SendCommand("I")
    End Sub

    Private Sub Button26_Click(sender As Object, e As EventArgs) Handles Button26.Click
        Dim cameras As VideoCaptureDeviceForm = New VideoCaptureDeviceForm
        If cameras.ShowDialog() = Windows.Forms.DialogResult.OK Then
            CAMERA = cameras.VideoDevice
            AddHandler CAMERA.NewFrame, New NewFrameEventHandler(AddressOf Captured)
            CAMERA.Start()
        End If
    End Sub

    Private Sub Captured(sender As Object, eventArgs As NewFrameEventArgs)
        bmp = DirectCast(eventArgs.Frame.Clone(), Bitmap)
        PictureBox1.Image = DirectCast(eventArgs.Frame.Clone(), Bitmap)
    End Sub


    Private Sub Button27_Click(sender As Object, e As EventArgs) Handles Button27.Click
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\" & TextBox4.Text & ".png")
    End Sub

    Public Function SaveImage(path As String)
        Try
            bmp = PictureBox1.Image
            bmp.Save(path, System.Drawing.Imaging.ImageFormat.Png)
        Catch
        End Try
    End Function

    Private Sub Button28_Click(sender As Object, e As EventArgs) Handles Button28.Click
        Dim delay_photo As Integer = 500
        'SendCommand("D 50")
        'SendCommand("S 1200")
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\0.png")
        Threading.Thread.Sleep(delay_photo)
        SendCommand("M Fb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\4.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M FFbb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\2.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M FbRl")
        Threading.Thread.Sleep(delay_photo)
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\1.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M RRll")
        Threading.Thread.Sleep(delay_photo)
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\3.png")
        Threading.Thread.Sleep(delay_photo)


        SendCommand("M RlRRBBLLFF")
        Threading.Thread.Sleep(1500)
        SaveImage("C:\Users\Vojta\Desktop\rc project\programm\python\images\calibration\5.png")
        Threading.Thread.Sleep(delay_photo)
        SendCommand("M FFLLBBRR")
    End Sub

    Private Sub Button21_Click(sender As Object, e As EventArgs) Handles Button21.Click
        Dim delay_photo As Integer = 800
        Dim path As String = "C:\Users\Vojta\Desktop\rc project\programm\python\images\scramble\"
        'SendCommand("D 150")
        'SendCommand("S 1000")


        SaveImage(path & "0.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M Fb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "1.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M Fb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "2.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M Fb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "3.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M FbRl")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "4.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M Rl")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "5.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M Rl")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "6.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M RlFbRl")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "7.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M RRll")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "8.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M RlfB")

        SendCommand("M RlFb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "9.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M FFbb")
        Threading.Thread.Sleep(delay_photo)
        SaveImage(path & "10.png")
        Threading.Thread.Sleep(delay_photo)

        SendCommand("M FbrL")
    End Sub
End Class
