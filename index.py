#myproject/Scripts/Activate
from flask import Flask,request,render_template
import pandas as pd
#from web.route import index

app=Flask(__name__)

@app.route('/', methods=["POST","GET"])
def index():
	if request.method == 'POST':
		next_page = request.form.get('button')
		if next_page == 'home':
			return render_template('index.html')
		elif next_page=='example':
			return render_template('example.html')
		elif next_page=='input':
			return render_template('input.html')
		elif next_page=='contact':
			return render_template('contact.html')
		elif next_page=="result":
			print("index")
			return render_template('result.html')
	return render_template('index.html')
	
@app.route('/example', methods=["POST","GET"])
def example():
	return render_template('example.html')

@app.route('/input', methods=["POST","GET"])
def input():
    if request.method=="POST":
        if request.form.get('result')=='result':
            sequence = request.form.get('sequence').upper()
            if len(sequence)!=0:
                print(1)
                sequence_lines = sequence.splitlines()
                for i in range(len(sequence_lines)):
                    for j in range(i+1,len(sequence_lines)):
			if sequence_lines[j].find('B')!=-1 or sequence_lines[j].find('J')!=-1 or sequence_lines[j].find('O')!=-1 or sequence_lines[j].find('U')!=-1 or sequence_lines[j].find('X')!=-1 or sequence_lines[j].find('Z')!=-1:
                            print("****")
                            return render_template('input.html')
                        if len(sequence_lines[i])!=len(sequence_lines[j]):
                            return render_template('input.html')
                sequence_html = '<p style="margin: 0%;">' + '</p><p style="margin: 0%;">'.join(sequence_lines) + '</p>'
                print(sequence_html)
                img=test(sequence_lines)
                return render_template('result.html', sequence=sequence_html,img=img)
                #time.sleep(0.5)
            else:
                print(2)
                return render_template('input.html')
            
    return render_template('input.html')

@app.route('/success', methods=["POST","GET"])
def success():
	return render_template('success.html')

import pandas as pd
import matplotlib.pyplot as plt
import logomaker as lm
def test(sequence):
    plt.ion()
    plt.ioff()
    #sequence = ['GDLGAGKTT','GDLGAGKTT','GPLGAGKTS','GDLGAGKTS','GDLGAGKTT','GDLGAGKTT','GEVGSGKTT','GELGAGKTT','GDLGAGKTT','GNLGAGKTT','GELGAGKTT','GTLGAGKTT','GDLGAGKTT','GDLGAGKTT','GDLGAGKTT','GDLGAGKTT','GDLGAGKTT']
    # create counts matrix
    ww_counts_df = lm.alignment_to_matrix(sequences=sequence, to_type='counts', characters_to_ignore='.-X')
    # filter based on counts
    num_seqs = ww_counts_df.sum(axis=1)
    pos_to_keep = num_seqs > len(sequence)/2
    ww_counts_df = ww_counts_df[pos_to_keep]
    ww_counts_df.reset_index(drop=True, inplace=True)
    # Create a custom color scheme dictionary
    color_scheme = {'F': [.16, .99, .18],
            'Y': [.04, .40, .05],
            'L': [.99, .60, .25],
            'V': [1.0, .80, .27],
            'I': [.80, .60, .24],
            'H': [.40, .02, .20],
            'W': [.42, .79, .42],
            'A': [.99, .60, .42],
            'S': [.04, .14, .98],
            'T': [.17, 1.0, 1.0],
            'M': [.80, .60, .80],
            'N': [.21, .40, .40],
            'Q': [.40, .41, .79],
            'R': [.59, .02, .04],
            'K': [.40, .20, .03],
            'E': [.79, .04, .22],
            'G': [.95, .94, .22],
            'D': [.99, .05, .11],
            'P': [.10, .61, .99],
            'C': [.09, .60, .60]}
    # Set the y-axis label
    ylabel = 'bits'
    # Create the logo figure
    logo_fig, logo_ax = plt.subplots()
    # Show the logo with the custom color scheme and y-axis label
    lm.Logo(ww_counts_df, ax=logo_ax, color_scheme=color_scheme)
    # Save the logo as an image
    output_path = 'static/dist/assets/out.png'
    plt.savefig(output_path, dpi=300)
    #plt.close(logo_fig)# Save the logo as an image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    plt.close(logo_fig)
    img_buffer.seek(0)

    # Convert the image to a base64-encoded string
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    img_html = f'<img style="max-width: 100%; height: auto;" class="col-md-8" src="data:image/png;base64,{img_str}"  alt="Example">'

    return img_html


@app.route('/contact', methods=["POST","GET"])
def contact():
	return render_template('contact.html')

@app.route('/result', methods=["POST","GET"])
def result():
	return render_template('result.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='80',debug=True)
