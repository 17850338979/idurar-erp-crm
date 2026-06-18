import React, { useState } from 'react';
import axios from 'axios';

const FinanceAssistant = () => {
    const [question, setQuestion] = useState('');
    const [month, setMonth] = useState('2024-06');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const handleQuery = async () => {
        setLoading(true);
        try {
            const res = await axios.post('http://localhost:8080/api/ai/finance/query', {
                question,
                month
            });
            setAnswer(res.data.answer);
        } catch (e) {
            alert('查询失败，请检查服务是否启动');
        }
        setLoading(false);
    };

    return (
        <div className="finance-assistant">
            <h2>AI财务助手</h2>
            <div className="form-group">
                <label>选择月份：</label>
                <input type="month" value={month} onChange={e => setMonth(e.target.value)} />
            </div>
            <div className="form-group">
                <label>你的问题：</label>
                <input 
                    type="text" 
                    value={question} 
                    onChange={e => setQuestion(e.target.value)}
                    placeholder="比如：这个月的办公支出有多少？"
                />
            </div>
            <button onClick={handleQuery} disabled={loading}>
                {loading ? '查询中...' : '咨询AI助手'}
            </button>
            {answer && (
                <div className="answer">
                    <h3>AI回答：</h3>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
};

export default FinanceAssistant;
