from aws_cdk import (
    # Duration,
    Stack,
    aws_events,
    aws_sqs,
    aws_sns,
    aws_events_targets
)
from constructs import Construct


class CdkSpikeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        rule_1 = aws_events.Rule(
            self,
            "ec2-executions",
            event_pattern= aws_events.EventPattern(
                source= ["aws.ec2"],
            ),
        )

        queue_1 = aws_sqs.Queue(
            self,
            "EC2Queue"
        )

        rule_1.add_target(
            aws_events_targets.SqsQueue(
                queue_1
            )
        )

        # The code that defines your stack goes here
        main_event_bus = aws_events.EventBus(
            self,
            "business-events-bus",
            event_bus_name="business-events"
        )

        rule_b_1 = aws_events.Rule(
            self,
            "be-ec2-sales",
            event_bus=main_event_bus,
            event_pattern= aws_events.EventPattern(
                source= ["aws.s3"],
            )
        )

        sns_sales = aws_sns.Topic(
            self,
            "salesTopic"
        )

        sns_warehouse = aws_sns.Topic(
            self,
            "warehouseInventory"
        )

        rule_b_1.add_target(
            aws_events_targets.SnsTopic(
                sns_sales
            )
        )

        rule_b_1.add_target(aws_events_targets.SnsTopic(
            sns_warehouse
        ))

        admin_event_bus = aws_events.EventBus(
            self,
            "admin-events-bus",
            event_bus_name="admin-events"
        )

        rule_a_1 = aws_events.Rule(
            self,
            "ec2-errors",
            event_bus=admin_event_bus,
            event_pattern= aws_events.EventPattern(
                source= ["aws.ec2"],
            )
        )

        rule_a_2 = aws_events.Rule(
            self,
            "s3-errors",
            event_bus=admin_event_bus,
            event_pattern= aws_events.EventPattern(
                source= ["aws.s3"],
            )
        )

        rule_a_3 = aws_events.Rule(
            self,
            "ecs-errors",
            event_bus=admin_event_bus,
            event_pattern= aws_events.EventPattern(
                source= ["aws.ecs"],
            )
        )
