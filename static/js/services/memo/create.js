async function createMemo(url, body_data) {
    const csrf_token = getCookie('csrfmiddlewaretoken')
    console.log(url);
    console.log(body_data)
    console.log(csrf_token)

    const response = await fetch(url, {
        method: 'POST',
        body: body_data
    });

    if (response.status === 403) {
        throw new Error("ログインしてください。");
    }

    
    const data = await response.json();

    return data;
}

