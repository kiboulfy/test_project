from rest_framework import serializers
from .models import Ad, ExchangeProposal

class AdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ad 
        fields = '__all__'
    



class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'


class ExchangeProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']

    def validate_ad_sender(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Вы можете использовать только свои объявления как отправителя.")
        return value


class ExchangeProposalUpdateSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(read_only=True)
    ad_receiver = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = serializers.CharField(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'comment', 'status']
    
