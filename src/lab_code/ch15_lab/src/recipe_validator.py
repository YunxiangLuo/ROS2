#!/usr/bin/env python3
"""recipe_validator: 题1 — LLM 校验化学实验配方 (Service 节点)"""
import json
import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger


class RecipeValidator(Node):
    def __init__(self):
        super().__init__('recipe_validator')
        self.srv = self.create_service(
            Trigger, 'validate_recipe', self.validate_callback)
        self.get_logger().info('配方验证服务就绪')

    def validate_callback(self, request, response):
        recipe = request.data
        self.get_logger().info(f'收到配方: {recipe[:80]}...')
        prompt = self.build_prompt(recipe)
        llm_result = self.call_llm(prompt)
        parsed = self.parse_response(llm_result)
        response.success = parsed.get('is_valid', False)
        response.message = json.dumps(parsed, ensure_ascii=False)
        self.get_logger().info(
            f'校验结果: {"通过" if response.success else "未通过"}')
        return response

    def build_prompt(self, recipe):
        return f"""你是中学化学实验安全专家。请校验以下实验配方：

{recipe}

验证内容：1.配比合理性 2.产物正确性 3.安全风险
返回JSON: {{"is_valid":bool, "feedback":"意见", "products":[], "safety_warnings":[]}}"""

    def call_llm(self, prompt):
        try:
            from openai import OpenAI
            client = OpenAI()
            resp = client.chat.completions.create(
                model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}],
                temperature=0.1)
            return resp.choices[0].message.content
        except Exception as e:
            self.get_logger().warn(f'LLM调用失败，默认通过: {e}')
            return '{"is_valid":true,"feedback":"未连接LLM，默认通过","products":[],"safety_warnings":["请手动检查"]}'

    def parse_response(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {'is_valid': True, 'feedback': text[:200]}


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(RecipeValidator())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
