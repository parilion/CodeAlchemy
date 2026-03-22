import { Card, Checkbox, Row, Col } from 'antd'
import { useProjectStore } from '../store/useProjectStore'

const MODULES = [
  { id: 'chat_assistant', name: '智能对话助手', desc: '查询型 + 知识问答型对话' },
  { id: 'rag_retrieval', name: 'RAG增强检索', desc: '基于业务文档的智能问答' },
  { id: 'smart_search', name: '智能语义搜索', desc: '与精准搜索并行，用户可选' },
  { id: 'smart_classify', name: '智能分类', desc: 'AI自动推荐分类标签' },
  { id: 'collaborative_filter', name: '协同过滤推荐', desc: '"看了此商品的用户还看了..."' },
]

export default function AIModuleSelector() {
  const { selectedModules, toggleModule } = useProjectStore()

  return (
    <Row gutter={[16, 16]}>
      {MODULES.map((m) => (
        <Col key={m.id} xs={24} sm={12} md={8}>
          <Card
            hoverable
            style={{
              border: selectedModules.includes(m.id) ? '2px solid #1677ff' : '1px solid #d9d9d9',
              cursor: 'pointer',
            }}
            onClick={() => toggleModule(m.id)}
          >
            <Checkbox
              checked={selectedModules.includes(m.id)}
              onChange={() => toggleModule(m.id)}
              style={{ marginBottom: 8, pointerEvents: 'none' }}
            >
              <strong>{m.name}</strong>
            </Checkbox>
            <p style={{ color: '#666', fontSize: 13, margin: 0 }}>{m.desc}</p>
          </Card>
        </Col>
      ))}
    </Row>
  )
}
