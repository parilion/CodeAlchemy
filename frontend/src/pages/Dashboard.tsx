import { Button, Card, Row, Col, Typography, Space } from 'antd'
import { RocketOutlined, CodeOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const nav = useNavigate()

  return (
    <div style={{ padding: '32px', maxWidth: 1000, margin: '0 auto' }}>
      <Typography.Title level={2} style={{ textAlign: 'center', marginBottom: 8 }}>
        AI赋能开发平台
      </Typography.Title>
      <Typography.Paragraph style={{ textAlign: 'center', color: '#666', marginBottom: 40 }}>
        为普通Java管理系统注入AI能力，生成高溢价学生作品
      </Typography.Paragraph>

      <Row gutter={[24, 24]}>
        <Col xs={24} md={12}>
          <Card
            hoverable
            style={{ height: 200, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
            onClick={() => nav('/upload')}
          >
            <Space direction="vertical" align="center" style={{ width: '100%' }}>
              <CodeOutlined style={{ fontSize: 48, color: '#1677ff' }} />
              <Typography.Title level={4} style={{ margin: 0 }}>代码增强模式</Typography.Title>
              <Typography.Text type="secondary">上传现有项目 → 注入AI能力 → 下载源码包</Typography.Text>
              <Button type="primary" onClick={(e) => { e.stopPropagation(); nav('/upload') }}>
                开始增强
              </Button>
            </Space>
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card
            hoverable
            style={{ height: 200, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
            onClick={() => nav('/template')}
          >
            <Space direction="vertical" align="center" style={{ width: '100%' }}>
              <RocketOutlined style={{ fontSize: 48, color: '#52c41a' }} />
              <Typography.Title level={4} style={{ margin: 0 }}>模板生成模式</Typography.Title>
              <Typography.Text type="secondary">输入需求描述 → 匹配模板 → 生成AI系统</Typography.Text>
              <Button type="primary" style={{ background: '#52c41a', borderColor: '#52c41a' }}
                onClick={(e) => { e.stopPropagation(); nav('/template') }}>
                从模板生成
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
