cd %~dp0..\..\..\
del /f "%userprofile%\Documents\Fiddler2\Scripts\CustomRules.js"
xcopy /y "%~dp0CustomRules.js" "%userprofile%\Documents\Fiddler2\Scripts"