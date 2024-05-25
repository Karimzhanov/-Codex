from django import forms

class VerifyCodeForm(forms.Form):
    email = forms.EmailField(label="Email")
    code = forms.CharField(label="Reset Code")
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
