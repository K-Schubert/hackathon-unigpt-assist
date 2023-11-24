from django import forms


class ChatBotForm(forms.Form):
	message = forms.CharField(
		label='',
		max_length=4096,
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter your message here'
			}
		)
	)
