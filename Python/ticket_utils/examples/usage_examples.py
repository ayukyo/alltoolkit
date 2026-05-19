"""
ticket_utils 使用示例

演示各种票据编号生成和使用方法
"""

from datetime import datetime
from mod import (
    TicketGenerator,
    generate_order_number,
    generate_invoice_number,
    generate_ticket_number,
    generate_refund_number,
    generate_tracking_number,
    generate_coupon_code,
    generate_batch_number,
    generate_receipt_number,
    parse_ticket_number,
    validate_luhn,
    generate_custom_ticket,
    batch_generate,
    ticket_info,
    SequentialTicketGenerator
)


def example_basic_ticket_generator():
    """基本票据生成器示例"""
    print("=== 基本票据生成器示例 ===\n")
    
    # 创建生成器
    gen = TicketGenerator(prefix="ORD", separator="-")
    
    # 流水号格式
    print("1. 流水号格式:")
    serial_ticket = gen.generate_serial()
    print(f"   {serial_ticket}")
    
    # 时间戳格式
    print("\n2. 时间戳格式:")
    timestamp_ticket = gen.generate_timestamp()
    print(f"   {timestamp_ticket}")
    
    # 带毫秒的时间戳
    print("\n3. 带毫秒的时间戳:")
    ms_ticket = gen.generate_timestamp(include_ms=True)
    print(f"   {ms_ticket}")
    
    # 带随机后缀
    print("\n4. 带随机后缀:")
    rand_ticket = gen.generate_timestamp(random_suffix=4)
    print(f"   {rand_ticket}")
    
    # 哈希格式
    print("\n5. 哈希格式:")
    hash_ticket = gen.generate_hash()
    print(f"   {hash_ticket}")
    
    # Luhn 校验位
    print("\n6. 带Luhn校验位:")
    luhn_ticket = gen.generate_luhn()
    print(f"   {luhn_ticket}")
    print(f"   验证: {validate_luhn(luhn_ticket.split('-')[1])}")


def example_specific_generators():
    """特定票据生成示例"""
    print("\n=== 特定票据生成示例 ===\n")
    
    # 订单号
    print("1. 订单号:")
    print(f"   普通: {generate_order_number()}")
    print(f"   带校验: {generate_order_number(include_check=True)}")
    
    # 发票号
    print("\n2. 发票号:")
    print(f"   当前年: {generate_invoice_number()}")
    print(f"   指定年: {generate_invoice_number(year=2025)}")
    
    # 工单号
    print("\n3. 工单号:")
    print(f"   {generate_ticket_number()}")
    
    # 退款单号
    print("\n4. 退款单号:")
    print(f"   {generate_refund_number()}")
    
    # 物流追踪号
    print("\n5. 物流追踪号:")
    print(f"   顺丰: {generate_tracking_number('SF')}")
    print(f"   圆通: {generate_tracking_number('YTO')}")
    print(f"   中通: {generate_tracking_number('ZTO')}")
    
    # 优惠券码
    print("\n6. 优惠券码:")
    print(f"   {generate_coupon_code()}")
    print(f"   长码: {generate_coupon_code(length=12)}")
    
    # 批次号
    print("\n7. 批次号:")
    print(f"   {generate_batch_number()}")
    
    # 收据号
    print("\n8. 收据号:")
    print(f"   {generate_receipt_number()}")


def example_custom_template():
    """自定义模板示例"""
    print("\n=== 自定义模板示例 ===\n")
    
    # 基本模板
    print("1. 基本模板:")
    template = "{prefix}-{date}-{serial}"
    print(f"   模板: {template}")
    print(f"   结果: {generate_custom_ticket(template, {'prefix': 'MYAPP'})}")
    
    # 随机数字模板
    print("\n2. 随机数字模板:")
    template = "{prefix}-{year}{month}{day}-{rand:6}"
    print(f"   模板: {template}")
    print(f"   结果: {generate_custom_ticket(template, {'prefix': 'ORD'})}")
    
    # 随机字母模板
    print("\n3. 随机字母模板:")
    template = "{prefix}-{rand_alpha:8}"
    print(f"   模板: {template}")
    print(f"   结果: {generate_custom_ticket(template, {'prefix': 'CODE'})}")
    
    # 混合模板
    print("\n4. 复杂混合模板:")
    template = "{prefix}-{year}-{rand_alnum:4}-{time}-{serial}"
    print(f"   模板: {template}")
    print(f"   结果: {generate_custom_ticket(template, {'prefix': 'TKT'})}")


def example_batch_generation():
    """批量生成示例"""
    print("\n=== 批量生成示例 ===\n")
    
    # 批量生成订单号
    print("1. 批量订单号 (10个):")
    orders = batch_generate(10, generate_order_number)
    for i, o in enumerate(orders[:5]):
        print(f"   {i+1}. {o}")
    print(f"   ... 共 {len(orders)} 个")
    
    # 批量生成优惠券码
    print("\n2. 批量优惠券码 (20个):")
    coupons = batch_generate(20, generate_coupon_code)
    for i, c in enumerate(coupons[:5]):
        print(f"   {i+1}. {c}")
    print(f"   ... 共 {len(coupons)} 个")
    
    # 验证唯一性
    print(f"\n   唯一性检查: {len(set(coupons))} / {len(coupons)} (100%唯一)")


def example_parse_and_validate():
    """解析和验证示例"""
    print("\n=== 解析和验证示例 ===\n")
    
    # 解析订单号
    print("1. 解析订单号:")
    order = generate_order_number()
    print(f"   订单号: {order}")
    info = parse_ticket_number(order)
    print(f"   解析结果:")
    print(f"     - 前缀: {info['prefix']}")
    print(f"     - 日期: {info['date']}")
    print(f"     - 序号: {info['serial']}")
    
    # 解析工单号
    print("\n2. 解析工单号:")
    ticket = generate_ticket_number()
    print(f"   工单号: {ticket}")
    info = parse_ticket_number(ticket)
    print(f"   解析结果:")
    print(f"     - 前缀: {info['prefix']}")
    print(f"     - 日期: {info['date']}")
    print(f"     - 时间: {info['time']}")
    print(f"     - 序号: {info['serial']}")
    
    # 获取票据信息
    print("\n3. 获取票据信息:")
    order = generate_order_number()
    info = ticket_info(order)
    print(f"   {order}")
    print(f"     - 类型: {info['type']}")
    print(f"     - 有效: {info['valid']}")
    
    # Luhn 校验
    print("\n4. Luhn校验:")
    test_numbers = ["79927398713", "4242424242424242", "1234567812345670"]
    for num in test_numbers:
        valid = validate_luhn(num)
        print(f"   {num}: {'有效' if valid else '无效'}")


def example_sequential_generator():
    """顺序生成器示例"""
    print("\n=== 顺序生成器示例 ===\n")
    
    # 创建顺序生成器
    gen = SequentialTicketGenerator(
        prefix="SEQ",
        separator="-",
        start_serial=1,
        serial_length=6
    )
    
    # 生成5个顺序票据
    print("1. 顺序生成票据:")
    for i in range(5):
        ticket = gen.generate()
        print(f"   {i+1}. {ticket}")
    
    # 预览下一个
    print("\n2. 预览下一个（不消耗）:")
    peek = gen.peek_next()
    print(f"   预览: {peek}")
    
    # 继续生成
    actual = gen.generate()
    print(f"   实际: {actual}")
    print(f"   预览=实际: {peek == actual}")
    
    # 获取统计
    print("\n3. 生成器统计:")
    stats = gen.get_stats()
    print(f"   当前序号: {stats['current_serial']}")
    print(f"   已生成数: {stats['generated_count']}")
    
    # 重置
    print("\n4. 重置生成器:")
    gen.reset(start_serial=1)
    print(f"   重置后第一个: {gen.generate()}")


def example_business_scenario():
    """业务场景示例"""
    print("\n=== 业务场景示例 ===\n")
    
    # 场景1: 电商订单流程
    print("1. 电商订单流程:")
    order = generate_order_number(prefix="ORD")
    print(f"   创建订单: {order}")
    
    # 发货
    tracking = generate_tracking_number("SF")
    print(f"   物流单号: {tracking}")
    
    # 需要退款
    refund = generate_refund_number(prefix="REF")
    print(f"   退款单号: {refund}")
    
    # 发票
    invoice = generate_invoice_number(prefix="INV")
    print(f"   发票号: {invoice}")
    
    # 场景2: 客服工单流程
    print("\n2. 客服工单流程:")
    
    # 创建工单生成器
    ticket_gen = SequentialTicketGenerator(prefix="CS", serial_length=4)
    
    # 客户投诉
    ticket1 = ticket_gen.generate()
    print(f"   投诉工单: {ticket1}")
    
    # 转交处理
    ticket2 = ticket_gen.generate()
    print(f"   转交工单: {ticket2}")
    
    # 结案
    print(f"   结案时共处理: {ticket_gen.get_stats()['generated_count']} 单")
    
    # 场景3: 营销活动优惠券
    print("\n3. 营销活动优惠券:")
    
    # 批量生成100个优惠券
    coupons = batch_generate(100, generate_coupon_code, prefix="SUMMER2024")
    print(f"   生成 {len(coupons)} 张优惠券")
    print(f"   示例:")
    for i in range(3):
        print(f"     {i+1}. {coupons[i]}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("ticket_utils 使用示例")
    print("=" * 50)
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    example_basic_ticket_generator()
    example_specific_generators()
    example_custom_template()
    example_batch_generation()
    example_parse_and_validate()
    example_sequential_generator()
    example_business_scenario()
    
    print("\n" + "=" * 50)
    print("示例运行完成")
    print("=" * 50)


if __name__ == "__main__":
    main()