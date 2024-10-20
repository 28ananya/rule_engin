document.getElementById('create-rule-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleName = document.getElementById('rule_name').value;
    const ruleString = document.getElementById('rule_string').value;
    
    const response = await fetch('/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_name: ruleName, rule_string: ruleString })
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('evaluate-rule-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleName = document.getElementById('evaluate_rule_name').value;
    const userData = document.getElementById('user_data').value;
    
    const response = await fetch('/evaluate_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_name: ruleName, data: JSON.parse(userData) })
    });

    const result = await response.json();
    alert('Eligible: ' + result.eligible);
});
