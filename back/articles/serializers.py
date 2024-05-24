from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User

# user
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# article list
class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    class CommentCountSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = '__all__'
    comments = CommentCountSerializer(read_only=True, many=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only= True)
    user = UserSimpleSerializer()
    class Meta:
        model = Article
        fields = '__all__'

# article detail
class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = '__all__'
    # user = serializers.ReadOnlyField(source='user.username')
    user = UserSimpleSerializer(read_only=True)
    comments = CommentDetailSerializer(read_only=True, many=True)
    class Meta:
        model = Article
        fields = '__all__'

# comment 관련 정보
class CommentSerializer(serializers.ModelSerializer):
    
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = '__all__'
    user = UserSimpleSerializer(read_only=True)
    # user = serializers.ReadOnlyField(source='user.username')
    article = ArticleTitleSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
   

