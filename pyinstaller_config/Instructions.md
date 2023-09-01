# Instructions for compilation

## Generate the Certificate

```Powershell
New-SelfSignedCertificate -Type Custom -Subject "CN=Paul Creusy" -KeyUsage DigitalSignature -FriendlyName "MCQMaker" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")
```

Cert thumbprint : A30811B9292BA9D9F3112E6011E300B5546A715A

## Get the list of certificates

```Powershell
Set-Location Cert:\CurrentUser\My
Get-ChildItem | Format-Table Subject, FriendlyName, Thumbprint
```

## Export the certificate

*Reboot the terminal before using this command*

```Powershell
$password = ConvertTo-SecureString -String <Your Password> -Force -AsPlainText 
Export-PfxCertificate -cert "Cert:\CurrentUser\My\A30811B9292BA9D9F3112E6011E300B5546A715A" -FilePath cert.pfx -Password $password
```

## Sign the package

### Sign with auto certificate

```Powershell
signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 MCQMaker.exe
```

### Sign with certificate in a specific file

```Powershell
signtool sign /f ./pyinstaller_config/cert.pfx /p <password> /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 ./MCQMaker_Windows/MCQMaker.exe
```