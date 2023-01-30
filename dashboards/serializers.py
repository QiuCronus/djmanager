import json
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from dashboards.models import Node

User = get_user_model()


def as_dict(value):
    try:
        return json.loads(value)
    except:
        return None


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = ("enabled", "alive_account_count", "pending_task_count", "updated_ts", "updated_at")

    def create(self, validated_data):
        now = datetime.now()
        validated_data["updated_ts"] = int(now.timestamp())
        validated_data["enabled"] = Node.INVALID
        return Node.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category = validated_data.get("category")
        domain = validated_data.get("domain")
        hostname = validated_data.get("hostname")
        label = validated_data.get("label")
        if (
                instance.category != category
                or instance.domain != domain
                or instance.hostname != hostname
                or instance.label != label
        ):
            return instance

        instance.cpu = validated_data.get("cpu", instance.cpu)
        instance.disk = validated_data.get("disk", instance.cpu)
        instance.memory = validated_data.get("memory", instance.cpu)

        pending_task_count = validated_data.get("pending_task_count", [])
        for task in pending_task_count:
            task_ = as_dict(task)
            if task_ and task_['status'] not in [2, 3, 4]:
                instance.pending_task_count += task_['count']

        account_details = validated_data.get("account_details", [])
        for account in account_details:
            account_ = as_dict(account)
            if account_ and account_['status'] in [0, 1]:
                instance.alive_account_count += account_['count']

        instance.save()
        return instance
