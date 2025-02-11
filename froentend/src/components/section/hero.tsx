'use client';
import { useEffect, useState } from 'react';

const cards = [
    { sub: 'Simplified', content: 'Complex tasks are now simple' },
    { sub: 'Boost Productivity', content: 'Perform Tasks in less time' },
    { sub: 'Facilitated learning', content: 'train anyone from anywhere' },
    { sub: 'Support', content: 'Now its 24/7 support' },
];

function Hero() {
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    useEffect(() => {
        rotateCards();
    }, [scrollY]);

    const rotateCards = () => {
        const cards = document.querySelectorAll<HTMLElement>('.card');
        let angle = 0;
        cards.forEach((card, index) => {
            if (card.classList.contains('away')) {
                card.style.transform = `translateY(-120vh) rotate(-48deg)`;
            } else {
                card.style.transform = `rotate(${angle}deg)`;
                angle = angle - 10;
                card.style.zIndex = `${cards.length - index}`;
            }
        });
    };

    useEffect(() => {
        const handleScroll = () => {
            const stackArea = document.querySelector('.stack-area');
            if (stackArea) {
                const distance = window.innerHeight * 0.5;
                const topVal = stackArea.getBoundingClientRect().top;
                let index = -1 * (topVal / distance + 1);
                index = Math.floor(index);

                const cards = document.querySelectorAll('.card');
                for (let i = 0; i < cards.length; i++) {
                    if (i <= index) {
                        cards[i].classList.add('away');
                    } else {
                        cards[i].classList.remove('away');
                    }
                }
                rotateCards();
            }
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <div className="stack-area w-full h-[300vh] relative flex ">
            <div className="h-screen flex-1 sticky top-0 flex flex-col items-center justify-center box-border">
                <div className="title text-[84px] font-poppins font-bold leading-[88px] w-[420px]">
                    Our Features
                </div>
                <div className="sub-title text-[14px] font-poppins mt-8 w-[420px]">
                    Lorem ipsum, dolor sit amet consectetur adipisicing elit. Sapiente qui
                    quis, facere, cupiditate, doloremque natus ex perspiciatis ratione hic
                    corrupti adipisci ea doloribus!
                    <br />
                    <button className="mt-5 px-6 py-3 bg-black text-white rounded-lg border-none outline-none cursor-pointer">
                        See More Details
                    </button>
                </div>
            </div>
            <div className="h-screen flex-1 items-center justify-center sticky top-0 ">
                {cards.map((card, i) => (
                    <div
                        key={i}
                        className={`card w-[350px] h-[350px] absolute rounded-lg transition-transform duration-500 ease-in-out top-[30vh] left-[30vh] transform -translate-x-1/2 -translate-y-1/2`}
                        style={{
                            backgroundColor: `rgb(${64 + i * 50}, ${122 - i * 30}, ${255 - i * 50})`,
                            zIndex: cards.length - i,
                        }}
                    >
                        <div className='m-5'>
                            <div className="sub text-[20px] font-poppins font-bold">{card.sub}</div>
                            <div className="content text-[44px] font-poppins font-bold leading-[54px]">{card.content}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Hero;