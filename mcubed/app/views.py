

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
    						title = 'Home',
    						h1 = "active",
    						h2 = "inactive",
    						h3 = "inactive")

@app.route('/about')
def about():
	return render_template('about.html',
							title = 'About',
							h1 = "inactive",
    						h2 = "active",
    						h3 = "inactive")

@app.route('/contact')
def contact():
	return render_template('contact.html',
							title = 'Contact',
							h1 = "inactive",
    						h2 = "inactive",
    						h3 = "active")	

@app.route('/one', methods=['GET', 'POST'])
def one():
    form = SiteForm(request.form)
    cur = connect_db()
    cur.execute('SELECT siteurl FROM crunchbase_startups LIMIT 1')
    randsite = cur.fetchone()

    if request.method == 'POST' and form.validate():
        flash('Processing for site: %s' %(form.url.data))
        return redirect('/one')

    return render_template('1.html', 
							title = 'Enter site',
							h1 = "inactive",
    						h2 = "inactive",
    						h3 = "inactive",
    						form = form,
    						randsite = randsite)	
							